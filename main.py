from finder import getAccounts
from followslist import getFollows
import utils


def exportFollowList(acc):
    print(f"Đang tải: {acc["fullName"]}...")
    name = utils.filter(acc["fullName"])
    with open(f"{name}follows.txt", "wb") as f:
        f.write(getFollows(acc["userGuid"], acc["readToken"]).encode())
    print("Thành công!")

try:

    print("Đang tìm các tài khoản...")

    accounts = list(getAccounts().values())

    print()

    for i, acc in enumerate(accounts):
        print(f"{i + 1}. {acc["fullName"]}")

    print(f"Đã tìm thấy {len(accounts)} tài khoản")

    if input("\nXuất ra danh sách theo dõi của tất cả tài khoản? (y/n) ").strip().lower() == "y":
        for acc in accounts:
            exportFollowList(acc)
        print("\nĐã xong")
    else:
        print()
        while True:
            inp = input("Nhập số thứ tự tài khoản muốn lưu (để trống để thoát): ").strip()
            if not inp: break
            try:
                acc = accounts[int(inp) - 1]
            except:
                print(inp, "không hợp lệ")
                continue
            exportFollowList(acc)
    
    try: input("Nhấn ENTER để thoát...")
    except: pass
except:
    import traceback; traceback.print_exc()
    try: input("Đã có lỗi xảy ra. Nhấn ENTER để thoát...")
    except: pass