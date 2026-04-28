# Multi-Tool Utility Pro ⚙️

Công cụ đa năng mạnh mẽ hỗ trợ chuyển đổi tệp, nén dữ liệu, sắp xếp thư mục và hơn thế nữa. Giao diện hiện đại, hỗ trợ kéo thả hàng loạt và xử lý song song chuyên nghiệp.

## 🌟 Tính năng nổi bật

- **Xử lý hàng loạt (Batch Processing) [NEW]**:
  - **Converter**: Chuyển đổi hàng trăm file cùng lúc sang định dạng đích chỉ với một cú click.
  - **Compressor**: Chọn nhiều file và thư mục khác nhau để đóng gói chung vào một tệp ZIP/RAR duy nhất.
- **Kéo & Thả toàn diện (Full Drag & Drop)**: Hỗ trợ kéo thả tệp, thư mục và URL trực tiếp vào cửa sổ ứng dụng ở tất cả các công cụ.
- **Chuyển đổi đa định dạng**:
  - **Hình ảnh**: JPG, PNG, WEBP, BMP.
  - **Âm thanh**: MP3, WAV, OGG, FLAC.
  - **Tài liệu**: Word (.docx) sang PDF/TXT, PDF sang Word/TXT.
- **Nén thư mục (Folder Compressor)**: Hỗ trợ ZIP (mặc định) và RAR (nếu máy có WinRAR).
- **Sắp xếp thư mục (Folder Organizer)**: Tự động phân loại file vào các thư mục Images, Documents, Videos, Audio...
- **Tìm file trùng lặp (Duplicate Finder)**: Quét nội dung (MD5 Hash) để phát hiện và xóa tệp/thư mục trùng lặp.
- **Tải xuống từ URL (URL Downloader)**: Tải tệp tốc độ cao, hỗ trợ kéo thả link trực tiếp.
- **Quản lý mật khẩu (Password Vault) [NEW]**: Lưu trữ và mã hóa thông tin tài khoản an toàn với Master Password.
- **Xem trước trực quan**:
  - Thumbnail hình ảnh.
  - Trình phát nhạc (Play/Stop) cho tệp âm thanh.
  - Xem thông tin chi tiết tệp văn bản.

---

## 🚀 Hướng dẫn sử dụng

### 1. Chuyển đổi hàng loạt (Batch Converter)
1. Chọn **🔄 Converter**.
2. **Kéo thả nhiều file** vào danh sách hoặc nhấn **📂 Thêm file**.
3. Chọn định dạng đích và **Thư mục đầu ra**.
4. Nhấn **🚀 BẮT ĐẦU BATCH CONVERT**.

### 2. Nén nhiều mục (Multi-Compressor)
1. Chọn **📦 Compressor**.
2. Kéo thả các file/thư mục cần nén vào danh sách.
3. Chọn định dạng (.zip hoặc .rar).
4. Nhấn **📦 BẮT ĐẦU NÉN**.

### 3. Sắp xếp & Quét trùng lặp
- Đơn giản chỉ cần **Kéo thả thư mục** cần xử lý vào cửa sổ ứng dụng và nhấn nút thực hiện.

---

## 🛠 Hướng dẫn cài đặt (Cho lập trình viên)

### 1. Yêu cầu
- Python 3.10+
- Windows OS

### 2. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 3. Đóng gói & Tạo Shortcut
- Để đóng gói file `.exe`:
```bash
pyinstaller Multi_File_Converter.spec --noconfirm
```
- Để cập nhật shortcut ra Desktop:
```bash
python create_shortcut.py
```

---

## 📝 Lưu ý
- **Word sang PDF**: Yêu cầu máy cài sẵn Microsoft Word.
- **Nén RAR**: Yêu cầu máy cài sẵn WinRAR.
- **FFmpeg**: Đã được tích hợp sẵn trong thư mục `bin/`.

---

**Phát triển bởi Minh Huy & Antigravity AI Coding Assistant** 🚀
