import re
import browser_cookie3
import coccoc

def getGuids(browser):
    guids = {}

    match browser:
        case "coccoc":
            coccoc.create()
            data = coccoc.cookies()
            coccoc.delete()

            for profile in data:
                cookies = data[profile]

                for host in cookies:
                    if re.match(r"^(f?\.)?nettruyen\w{1,8}\.com$", host) == None:
                        continue
                    
                    coo = cookies[host]
                    if "comicvisitor" in coo and guids.get(coo["comicvisitor"], "") == "":
                        guids[coo["comicvisitor"]] = coo[".ASPXAUTH"] if ".ASPXAUTH" in coo else ""
        case _:
            cookies = getattr(browser_cookie3, browser)()._cookies

            for host in cookies:
                if re.match(r"^(f?\.)?nettruyen\w{1,8}\.com$", host) == None:
                    continue

                for coo in cookies[host].values():
                    if "comicvisitor" in coo and guids.get(coo["comicvisitor"].value, "") == "":
                        guids[coo["comicvisitor"].value] = coo[".ASPXAUTH"].value if ".ASPXAUTH" in coo else ""
    
    return guids
