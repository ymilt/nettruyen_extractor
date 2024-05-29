import pintruyen
import finder
import time

from concurrent.futures import ThreadPoolExecutor


def extractFollows(userguid, fname="followlist.txt"):
    print("Đang tải danh sách theo dõi...")

    load = {
        "run": True,
        "pages": 0
    }

    def proc_page(p):
        print(f"Đang tải trang {p}...")
        if not load["run"]:
            return
        follow_page = pintruyen.API.Comic.getFollows(userguid, p)
        if not len(follow_page): 
            load["run"] = False
            return
        load[p] = follow_page
        load["pages"] += 1

    workers = 3
    wait_time = workers * 4.5

    with ThreadPoolExecutor(workers) as exe:
        i = 1
        while load["run"]:
            load["pages"] = 0
            ts = time.time()

            for _ in range(workers):
                exe.submit(proc_page, i + _)

            while load["run"] and load["pages"] < workers:
                if time.time() - ts > wait_time:
                    # Timeout
                    return ""
                time.sleep(.05)

            i += workers

    load.pop("run"), load.pop("pages")

    comics = []

    for key in sorted(load.keys()):
        comics.extend(load[key])


    with open(fname, "w", encoding="utf-8") as f:
        f.write("\n".join(map(lambda i: f"{i + 1}. {comics[i].name}{' - ' + comics[i].lastViewChapter.title if comics[i].lastViewChapter else ''}", range(len(comics)))))

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

def extractByGuid():
    guid = input("Nhập GUID: ").strip()
    extractFollows(guid)

try:
    print("Các chế độ:")
    print("1. Đăng nhập để tải danh sách theo dõi")
    print("2. Tìm kiếm tài khoản trên trình duyệt")
    print("3. Nhập GUID tài khoản\n")

    mode = input("Mời chọn: ").strip()
    print()

    match mode:
        case "1":
            extractByLogin()
        case "2":
            extractByCookies()
        case "3":
            extractByGuid()
        case _:
            print("Chế độ không tồn tại")

    input("\nNhấn ENTER để thoát...")
except KeyboardInterrupt:
    pass
except:
    try: input("Đã có lỗi xảy ra. Nhấn ENTER để thoát...")
    except: pass