# Multi File Converter Tool ⚙️

Công cụ chuyển đổi định dạng tệp tin đa năng, giao diện thân thiện, hỗ trợ kéo thả và xem trước nội dung.

## 🌟 Tính năng nổi bật

- **Chuyển đổi đa định dạng**:
  - **Hình ảnh**: JPG, PNG, WEBP, BMP.
  - **Âm thanh**: MP3, WAV, OGG, FLAC.
  - **Tài liệu**: Word (.docx) sang PDF/TXT, PDF sang Word/TXT.
- **Giao diện hiện đại**: Chia bố cục thông minh với khung xem trước (Preview) tiện lợi.
- **Kéo & Thả (Drag & Drop)**: Hỗ trợ kéo tệp trực tiếp từ thư mục vào ứng dụng.
- **Xem trước trực quan**:
  - Xem ảnh Thumbnail.
  - Đọc nội dung văn bản đầu trang.
  - Trình phát nhạc (Play/Stop) để nghe thử tệp âm thanh.
- **Tiện lợi**: Đã được đóng gói thành file `.exe` chạy ngay không cần cài đặt môi trường.

---

## 🚀 Hướng dẫn sử dụng (Cho người dùng)

1. **Mở ứng dụng**: Chạy file `Multi_File_Converter.exe` (hoặc Shortcut trên Desktop).
2. **Chọn file đầu vào**:
   - Nhấn nút **📂 Chọn...** ở dòng đầu tiên.
   - Hoặc đơn giản là **Kéo tệp tin** của bạn và thả vào bất kỳ đâu trên cửa sổ ứng dụng.
3. **Xem trước (Tùy chọn)**:
   - Nếu là ảnh, bạn sẽ thấy hình thu nhỏ.
   - Nếu là nhạc, hãy nhấn **▶ Phát thử (Play)** để nghe.
   - Nếu là văn bản, nội dung tóm tắt sẽ hiện ở khung bên phải.
4. **Chọn định dạng đích**: Chọn đuôi file bạn muốn chuyển đổi sang ở danh sách thả xuống.
5. **Chọn nơi lưu**: Mặc định phần mềm sẽ gợi ý lưu cùng thư mục với file gốc, bạn có thể nhấn **📁 Chọn...** để đổi chỗ khác.
6. **Bắt đầu**: Nhấn nút **🚀 BẮT ĐẦU CONVERT** và đợi thông báo thành công!

---

## 🛠 Hướng dẫn cài đặt (Cho lập trình viên)

Nếu bạn muốn chạy từ mã nguồn hoặc phát triển thêm:

### 1. Yêu cầu hệ thống
- Python 3.10 trở lên.
- Windows OS (Do sử dụng `pywin32` cho việc chuyển Word sang PDF).

### 2. Cài đặt thư viện
Mở Terminal tại thư mục dự án và chạy lệnh:
```bash
pip install Pillow pydub docx2pdf pdf2docx python-docx PyPDF2 pygame-ce tkinterdnd2
```

### 3. Chạy ứng dụng
```bash
python main.py
```

### 4. Đóng gói file .exe
Sử dụng PyInstaller:
```bash
pyinstaller --noconfirm --noconsole --name "Multi_File_Converter" --collect-all tkinterdnd2 --collect-all pygame --add-data "bin;bin" main.py
```

---

## 📝 Lưu ý
- Để chuyển đổi định dạng **Word sang PDF**, máy tính của bạn cần cài đặt sẵn phần mềm Microsoft Word.
- Tính năng chuyển đổi âm thanh đã được tích hợp sẵn lõi FFmpeg trong thư mục `bin/`, bạn không cần cài đặt thêm gì bên ngoài.

---
**Phát triển bởi Antigravity AI Coding Assistant** 🚀