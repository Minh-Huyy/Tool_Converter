import os
import mimetypes
from service import ConverterService

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
                if mime_type.startswith("image/"):
                    is_image = True
                elif mime_type.startswith("audio/"):
                    is_audio = True
                elif mime_type == "application/pdf":
                    is_document = True

            # Fallback nếu hệ điều hành không quét ra mimetype
            if not (is_image or is_audio or is_document):
                if ext in cls.SUPPORTED_IMAGE:
                    is_image = True
                elif ext in cls.SUPPORTED_AUDIO:
                    is_audio = True
                elif ext in cls.SUPPORTED_DOCUMENT:
                    is_document = True

            # Điều hướng đến Service
            if is_image:
                return ConverterService.convert_image(input_path, output_path)
            elif is_audio:
                return ConverterService.convert_audio(input_path, output_path)
            elif is_document:
                return ConverterService.convert_document(input_path, output_path)
            else:
                return False, f"Hệ thống không hỗ trợ convert file loại '{ext}'."

        except Exception as e:
            return False, f"Lỗi hệ thống Controller: {str(e)}"
