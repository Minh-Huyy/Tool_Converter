# Multi File Converter Tool ⚙️

Công cụ chuyển đổi định dạng tệp tin đa năng, giao diện thân thiện, hỗ trợ kéo thả và xem trước nội dung.

## 🌟 Tính năng nổi bật

- **Chuyển đổi đa định dạng**:
  - **Hình ảnh**: JPG, PNG, WEBP, BMP.
  - **Âm thanh**: MP3, WAV, OGG, FLAC.
  - **Tài liệu**: Word (.docx) sang PDF/TXT, PDF sang Word/TXT.
- **Sắp xếp thư mục (Folder Organizer)**: Tự động phân loại file vào các thư mục Images, Documents, Videos, Audio, Archives... giúp dọn dẹp không gian lưu trữ.
- **Tìm file trùng lặp (Duplicate Finder)**: Quét và phát hiện các file trùng lặp nội dung (dựa trên mã Hash MD5), hỗ trợ xóa nhanh các bản sao để tiết kiệm bộ nhớ.
- **Tải xuống từ URL (URL Downloader)**: Tải tệp tin từ internet thông qua URL, hỗ trợ streaming cho tệp lớn và tự động nhận diện tên file.
- **Giao diện Dashboard hiện đại**: Thanh điều hướng bên trái (Sidebar) giúp chuyển đổi giữa các công cụ chuyên nghiệp.
- **Kéo & Thả (Drag & Drop)**: Hỗ trợ kéo tệp trực tiếp từ thư mục vào ứng dụng.
- **Xem trước trực quan**:
  - Xem ảnh Thumbnail.
  - Đọc nội dung văn bản đầu trang.
  - Trình phát nhạc (Play/Stop) để nghe thử tệp âm thanh.
- **Tiện lợi**: Đã được đóng gói thành file `.exe` chạy ngay không cần cài đặt môi trường.

---

## 🚀 Hướng dẫn sử dụng (Cho người dùng)

### 1. Chuyển đổi File (Converter)
1. Chọn công cụ **🔄 Converter** từ thanh Sidebar.
2. Nhấn nút **📂 Chọn...** hoặc **Kéo tệp tin** thả vào ứng dụng.
3. Chọn định dạng đích và nơi lưu, sau đó nhấn **🚀 BẮT ĐẦU CONVERT**.

### 2. Sắp xếp Thư mục (Organizer)
1. Chọn công cụ **📂 Organizer** từ thanh Sidebar.
2. Chọn thư mục cần dọn dẹp.
3. Nhấn **⚡ SẮP XẾP NGAY** để tự động đưa file vào các thư mục con tương ứng.

### 3. Tìm File trùng lặp (Duplicate Finder)
1. Chọn công cụ **🔍 Duplicate Finder** từ thanh Sidebar.
2. Chọn thư mục cần quét.
3. Nhấn **🔍 QUÉT FILE TRÙNG**. Hệ thống sẽ đánh dấu các bản sao (màu cam) và giữ lại bản gốc (màu xanh).
4. Nhấn **🗑️ XÓA CÁC BẢN SAO** để xóa sạch dữ liệu thừa.

### 4. Tải xuống từ URL (Downloader)
1. Chọn công cụ **⬇️ Downloader** từ thanh Sidebar.
2. Nhập (hoặc dán) đường dẫn **URL** của tệp tin cần tải.
3. Chọn thư mục lưu tệp (mặc định là Downloads).
4. Nhấn **🚀 BẮT ĐẦU TẢI XUỐNG**. Hệ thống sẽ hiển thị thanh tiến trình và báo cáo khi hoàn tất.

---

## 🛠 Hướng dẫn cài đặt (Cho lập trình viên)

Nếu bạn muốn chạy từ mã nguồn hoặc phát triển thêm:

### 1. Yêu cầu hệ thống
- Python 3.10 trở lên.
- Windows OS (Do sử dụng `pywin32` cho việc chuyển Word sang PDF).

### 2. Cài đặt thư viện
Mở Terminal tại thư mục dự án và chạy lệnh:
```bash
pip install Pillow pydub docx2pdf pdf2docx python-docx PyPDF2 pygame-ce tkinterdnd2 requests
```

### 3. Chạy ứng dụng
```bash
python main.py
```

### 4. Đóng gói file .exe
Sử dụng PyInstaller:
```bash
pyinstaller Multi_File_Converter.spec --noconfirm
```

---

## 📝 Lưu ý
- Để chuyển đổi định dạng **Word sang PDF**, máy tính của bạn cần cài đặt sẵn phần mềm Microsoft Word.
- Tính năng chuyển đổi âm thanh đã được tích hợp sẵn lõi FFmpeg trong thư mục `bin/`, bạn không cần cài đặt thêm gì bên ngoài.

---

**Phát triển bởi Minh Huy & Antigravity AI Coding Assistant** 🚀
