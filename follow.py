import pintruyen
import finder


def extractFollows(userguid, fname="followlist.txt"):
    print("Đang tải danh sách theo dõi...")

    comics = []

    page = 1

    while True:
        print(f"Đang tải trang {page}...")
        follow_page = pintruyen.API.Comic.getFollows(userguid, page)
        if not len(follow_page): break
        comics.extend(follow_page)
        page += 1

    with open(fname, "w", encoding="utf-8") as f:
        f.write("\n".join(map(lambda i: f"{i + 1}. {comics[i].name}{' - ' + comics[i].lastViewChapter.title if comics[i].lastViewChapter else ""}", range(len(comics)))))

        print(f"Đã lưu \"{fname}\"!")


def extractByLogin():
    print("Đăng nhập để tải danh sách theo dõi\n")

    while True:
        try: email = input("Email: ")
        except: print("Không hợp lệ!\n"); continue
        try: password = input("Mật khẩu: ")
        except: print("Không hợp lệ!\n"); continue

        try:
            print("\nĐang đăng nhập...")
            user = pintruyen.UserInfo.fromCredential(email, password)
            break
        except: print("\nEmail / Mật khẩu sai!\n"); continue

    print("Đăng nhập thành công!\n")

    extractFollows(user.guid)

def extractByCookies():
    print("Đang tìm tài khoản")

    guids = {}
    for browser in ["chrome", "firefox", "librewolf", "opera", "opera_gx", "edge", "chromium", "brave", "vivaldi", "safari", "coccoc"]:
        try:
            guids.update(finder.getGuids(browser))
        except: continue

    guids = list(guids.keys())
    
    print(f"Tìm thấy {len(guids)} tài khoản")
    print(f"Đang xuất...\n")

    for i, guid in enumerate(guids):
        extractFollows(guid, f"follows{i + 1}.txt")


try:
    print("Các chế độ:")
    print("1. Đăng nhập để tải danh sách theo dõi")
    print("2. Tìm kiếm tài khoản trên trình duyệt")

    match input("Mời chọn: ").strip():
        case "1":
            extractByLogin()
        case "2":
            extractByCookies()
        case _:
            print("Chế độ không tồn tại")

    input("\nNhấn ENTER để thoát...")
except KeyboardInterrupt:
    pass
except:
    try: input("Đã có lỗi xảy ra. Nhấn ENTER để thoát...")
    except: pass