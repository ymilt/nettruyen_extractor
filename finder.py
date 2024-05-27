import ujson as json, re
from curl_cffi import requests
import browser_cookie3

def getInfo(guid, aspxauth):
    return json.loads(requests.get("https://f.nettruyenvv.com/Comic/Services/ComicService.asmx/CheckAuth", headers={
        "Host": "f.nettruyenvv.com",
        "Cookie": f"comicvisitor={guid}; .ASPXAUTH={aspxauth}",
    }, impersonate="chrome124").content)

def lt(d1: dict, d2: dict):
    return sum(map(bool, d1.values())) < sum(map(bool, d2.values()))

def getGuids(browser):
    cookies = getattr(browser_cookie3, browser)()._cookies
    guids = {}

    for host in cookies:
        if re.match(r"^(f?\.)?nettruyen\w{1,8}\.com$", host) == None:
            continue
        coo = cookies[host]["/"]
        if "comicvisitor" in coo:
            guids[coo["comicvisitor"].value] = coo[".ASPXAUTH"].value if ".ASPXAUTH" in coo else ""
    
    return guids

def getAccounts():
    users = {}
    unknowns = 0
    
    for browser in ["chrome", "firefox", "librewolf", "opera", "opera_gx", "edge", "chromium", "brave", "vivaldi", "safari"]:
        try: 
            guids = getGuids(browser)
        except: continue

        for g in guids:
            info = getInfo(g, guids[g])
            if not info["userGuid"]: continue

            name = info.get("fullName", None)
            if type(name) != str: unknowns += 1; info["fullName"] = f"[UNKNOWN USER no.{unknowns}]"

            guid = info["userGuid"]
            if guid not in users or lt(users[guid], info):
                users[info["userGuid"]] = info

    return users