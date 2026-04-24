import os
import mimetypes
from .service import ConverterService

class ConverterController:
    SUPPORTED_IMAGE = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    SUPPORTED_AUDIO = {".mp3", ".wav", ".ogg", ".flac"}
    SUPPORTED_DOCUMENT = {".docx", ".pdf"}

    @classmethod
    def handle_convert(cls, input_path: str, output_path: str) -> tuple[bool, str]:
        if not input_path or not output_path:
            return False, "Vui lòng chọn đầy đủ file nguồn và nơi lưu mới."
        
        _, ext = os.path.splitext(input_path)
        ext = ext.lower()

        try:
            mime_type, _ = mimetypes.guess_type(input_path)
            is_image = False
            is_audio = False
            is_document = False

            if mime_type:
                if mime_type.startswith("image/"): is_image = True
                elif mime_type.startswith("audio/"): is_audio = True
                elif mime_type == "application/pdf": is_document = True

            if not (is_image or is_audio or is_document):
                if ext in cls.SUPPORTED_IMAGE: is_image = True
                elif ext in cls.SUPPORTED_AUDIO: is_audio = True
                elif ext in cls.SUPPORTED_DOCUMENT: is_document = True

            if is_image: return ConverterService.convert_image(input_path, output_path)
            elif is_audio: return ConverterService.convert_audio(input_path, output_path)
            elif is_document: return ConverterService.convert_document(input_path, output_path)
            else: return False, f"Hệ thống không hỗ trợ convert file loại '{ext}'."

        except Exception as e:
            return False, f"Lỗi hệ thống Controller: {str(e)}"

    @classmethod
    def handle_batch_convert(cls, input_paths: list[str], output_dir: str, target_ext: str) -> tuple[bool, str]:
        if not input_paths or not output_dir or not target_ext:
            return False, "Thiếu thông tin đầu vào (files, folder hoặc định dạng)."
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        success_count = 0
        error_count = 0
        
        for in_path in input_paths:
            file_name = os.path.basename(in_path)
            name_only, _ = os.path.splitext(file_name)
            out_path = os.path.join(output_dir, f"{name_only}_converted.{target_ext}")
            
            success, _ = cls.handle_convert(in_path, out_path)
            if success:
                success_count += 1
            else:
                error_count += 1
                
        return True, f"Hoàn tất! Thành công: {success_count}, Thất bại: {error_count}."
