# Nettruyen Extractor
Tải về danh sách theo dõi và lịch sử (sắp) đọc truyện từ nettruyen
> [!NOTE]
> Cập nhật: App đã hỗ trợ Cốc Cốc
# Usages
- Tự động tìm các tài khoản đã đăng nhập trên máy và tải về danh sách theo dõi
- Cho phép đăng nhập để lấy dữ liệu
- Nhập GUID để tải truyện ([hướng dẫn](#cách-lấy-guid))

App có 3 chế độ cho phép đăng nhập để lấy list theo dõi hoặc tự động tìm tài khoản đã từng đăng nhập trên máy tính. Chạy app và chọn 1 trong 3 chế độ + đợi là xong.

> [!WARNING]
> Vui lòng đóng trình duyệt trước khi sử dụng app để đảm bảo app hoạt động ổn định.
> Với một số trình duyệt như Chrome, Edge, Cốc Cốc,... thì có thể bạn cần phải tắt cả chương trình chạy ngầm

[Tải về app](#download)

## Cách lấy GUID
vào https://f.nettruyen(vv/tt/hh/...).com/

1. ctrl + shift + i mở devtools
2. Tìm "Application" trên thanh trên cùng, nhấn vào
3. Nhìn qua bên trái tìm "Cookies" rồi chọn mục có tên giống với link https://f.nettruyen(vv/tt/hh/...).com/
4. Copy giá trị của hàng tại cột "value" mà có giá trị của hàng đó tại cột "name" là "comicvisitor"

# Download
Bản mới nhất ở [đây](https://raw.githubusercontent.com/ymilt/nettruyen_extractor/main/dist/follow.exe) (15mb)
# How Does It Work
App sử dụng api chính thức từ app của nettruyen. Tham khảo thêm ở [đây](pintruyen.py)
# Build
Requires Python 3.12 and Pyinstaller

```bash
pip install -r requirements.txt
```

For the new version
```bash
pyinstaller follow.spec
```
# Issue
Please open a github issue
# Contributing
Very appreciated!
