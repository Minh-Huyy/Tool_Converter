import os
from PIL import Image, UnidentifiedImageError
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

class ConverterService:
    @staticmethod
    def convert_image(input_path: str, output_path: str) -> tuple[bool, str]:
        if not os.path.exists(input_path):
            return False, "File hình ảnh nguồn không tồn tại."
        try:
            with Image.open(input_path) as img:
                out_ext = os.path.splitext(output_path)[1].lower()
                
                # Cần xử lý ảnh trong suốt (RGBA) nếu chọn xuất thành JPG
                if img.mode in ("RGBA", "LA", "P") and out_ext in (".jpg", ".jpeg"):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    mask = img.split()[3] if img.mode == "RGBA" else None
                    if mask:
                        background.paste(img, mask=mask)
                    else:
                        background.paste(img)
                    img = background
                elif img.mode != "RGB" and out_ext in (".jpg", ".jpeg"):
                    img = img.convert("RGB")

                img.save(output_path)
            return True, "Convert hình ảnh thành công! ✅"
            
        except UnidentifiedImageError:
            return False, "Định dạng ảnh không được hỗ trợ hoặc file hỏng."
        except OSError as e:
            return False, f"Lỗi hệ thống tập tin (I/O error): {e}"
        except Exception as e:
            return False, f"Lỗi không xác định: {e}"

    @staticmethod
    def convert_audio(input_path: str, output_path: str) -> tuple[bool, str]:
        if not os.path.exists(input_path):
            return False, "File âm thanh nguồn không tồn tại."
        try:
            audio = AudioSegment.from_file(input_path)
            
            out_format = os.path.splitext(output_path)[1].lower().replace(".", "")
            if out_format not in ["mp3", "wav", "ogg"]:
                return False, f"Định dạng ({out_format}) chưa được hỗ trợ export."

            audio.export(output_path, format=out_format)
            return True, "Convert âm thanh thành công! ✅"
            
        except CouldntDecodeError:
            return False, "File âm thanh hỏng hoặc bị mã hoá không xác định."
        except FileNotFoundError:
            return False, ("Không tìm thấy Engine FFmpeg trên máy. \n\n"
                           "Vui lòng cài đặt FFmpeg và cấu hình Environment PATH, "
                           "đây là yêu cầu bắt buộc của thư viện Pydub.")
        except Exception as e:
            return False, f"Lỗi chưa xác định: {e}"
