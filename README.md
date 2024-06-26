# Nettruyen Extractor
Tải về danh sách theo dõi và lịch sử (sắp) đọc truyện từ nettruyen

Xem thêm bản web ở [đây](https://github.com/ymilt/nettruyen_extractor_web)


> [!CAUTION]
> Do app đã dead hoàn toàn nên giờ repo này sẽ được archive

# Usages
- Tự động tìm các tài khoản đã đăng nhập trên máy và tải về danh sách theo dõi
- Cho phép đăng nhập để lấy dữ liệu
- Nhập GUID để tải truyện ([hướng dẫn](#cách-lấy-guid))

Chạy app và chọn 1 trong 3 chế độ + đợi là xong.

> [!TIP]
> Vui lòng đóng trình duyệt trước khi sử dụng app để đảm bảo app hoạt động ổn định.
> Với một số trình duyệt như Chrome, Edge, Cốc Cốc,... thì có thể bạn cần phải [tắt chương trình chạy ngầm](https://quantrimang.com/cong-nghe/cach-tang-toc-windows-10-bang-cach-tat-ung-dung-chay-ngam-142153)

[***Tải về App***](#download)

> [!WARNING]
> Trên một số trình diệt virus sẽ báo **[file](dist/follow.exe) có virus**. Lưu ý rằng đây chỉ là thông báo sai do Pyinstaller được sử dụng để tạo file exe gây ra nhầm lẫn. Đọc thêm ở [đây<sub>tiếng Anh</sub>](https://coderslegacy.com/pyinstaller-exe-detected-as-virus-solutions/). Tham khảo hướng dẫn khôi phục app: [Windows](https://www.itechtics.com/restore-quarantined-files/#how-to-restore-windows-defender-quarantined-files), [Avast](https://support.avast.com/en-us/article/Use-Antivirus-Quarantine/#pc), [Malwarebytes](https://support.malwarebytes.com/hc/en-us/articles/360038479214-Restore-or-delete-quarantined-items-in-Malwarebytes-for-Windows-v4), [Bitdefender](https://www.bitdefender.com/consumer/support/answer/2092/#scroll-to-heading-0)

## Cách lấy GUID
vào https://f.nettruyen(vv/tt/hh/...).com/

1. ctrl + shift + i mở devtools
2. Tìm "Application" trên thanh trên cùng, nhấn vào
3. Nhìn qua bên trái tìm "Cookies" rồi chọn mục có tên giống với link https://f.nettruyen(vv/tt/hh/...).com/
4. Copy giá trị của hàng tại cột "value" mà có giá trị của hàng đó tại cột "name" là "comicvisitor"

> [!CAUTION]
> Đây là mã tài khoản của bạn. Tuyệt đối **KHÔNG CHIA SẺ VỚI AI KHÁC**

# Download
Bản mới nhất ở [đây](dist/follow.exe) (15mb)

# How Does It Work
App sử dụng api chính thức từ app của nettruyen. Tham khảo thêm ở [đây](pintruyen.py)

# Build
Requires Python 3.12 and Pyinstaller. You should build it inside a virtual environment to reduce the size of the executable

```bash
pip install -r requirements.txt
pyinstaller follow.spec
```

# Issue
Please open a github issue

# Contributing
Any contribution are very appreciated

## Porting

This library uses [curl_cffi](https://github.com/yifeikong/curl_cffi) to bypass Cloudflare

For the C language, have a look at [curl-impersonate](https://github.com/lwthiker/curl-impersonate)