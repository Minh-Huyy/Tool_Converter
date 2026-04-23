import os
import sys
from PIL import Image, UnidentifiedImageError
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
import docx
from docx2pdf import convert as docx_to_pdf
from pdf2docx import Converter as PdfConverter
from PyPDF2 import PdfReader

# Cấu hình đường dẫn FFmpeg/FFprobe
if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
    bin_dir = os.path.join(bundle_dir, "bin")
else:
    bin_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "bin")

if os.path.exists(bin_dir):
    os.environ["PATH"] += os.pathsep + bin_dir

class ConverterService:
    @staticmethod
    def convert_image(input_path: str, output_path: str) -> tuple[bool, str]:
        if not os.path.exists(input_path):
            return False, "File hình ảnh nguồn không tồn tại."
        try:
            with Image.open(input_path) as img:
                out_ext = os.path.splitext(output_path)[1].lower()
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
        except Exception as e:
            return False, f"Lỗi âm thanh: {e}"

    @staticmethod
    def convert_document(input_path: str, output_path: str) -> tuple[bool, str]:
        if not os.path.exists(input_path):
            return False, "File tài liệu nguồn không tồn tại."
        try:
            in_ext = os.path.splitext(input_path)[1].lower()
            out_ext = os.path.splitext(output_path)[1].lower()
            if in_ext == ".docx":
                if out_ext == ".pdf":
                    docx_to_pdf(input_path, output_path)
                    return True, "Convert Word sang PDF thành công! ✅"
                elif out_ext == ".txt":
                    doc = docx.Document(input_path)
                    with open(output_path, "w", encoding="utf-8") as f:
                        for p in doc.paragraphs:
                            f.write(p.text + "\n")
                    return True, "Trích xuất Text thành công! ✅"
            elif in_ext == ".pdf":
                if out_ext == ".docx":
                    cv = PdfConverter(input_path)
                    cv.convert(output_path)
                    cv.close()
                    return True, "Convert PDF sang Word thành công! ✅"
                elif out_ext == ".txt":
                    reader = PdfReader(input_path)
                    with open(output_path, "w", encoding="utf-8") as f:
                        for page in reader.pages:
                            text = page.extract_text()
                            if text: f.write(text + "\n")
                    return True, "Trích xuất Text từ PDF thành công! ✅"
            return False, f"Không hỗ trợ {in_ext} sang {out_ext}."
        except Exception as e:
            return False, f"Lỗi tài liệu: {e}"
