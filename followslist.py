from curl_cffi import requests
import ujson
from bs4 import BeautifulSoup


def getFollows(userGuid, token):

    def url(page):
        return f"https://f.nettruyenvv.com/Comic/Services/ComicService.asmx/GetFollowedPageComics?userGuid={userGuid}&token={token}&page={page}&loadType=2"

    def extractComic(html):
        comics = []

        doc = BeautifulSoup(html, "html.parser")
        
        doc = doc.find("tbody")

        for manga in doc.find_all("tr", recursive=False):
            name = manga.find("a", class_="comic-name")
            time = name.find_next("time").text

            comics.append([name.text, time])

        return comics


    fdata = ujson.loads(requests.get(url(1), impersonate="chrome124").content)

    totpage = BeautifulSoup(fdata["pagerHtml"], "html.parser").find("li").text.strip()
    totpage = int(totpage[totpage.rfind("of") + 2:])

    pages = [fdata["followedListHtml"]]

    for u in map(url, range(2, totpage + 1)):
        pages.append(ujson.loads(requests.get(u, impersonate="chrome124").content)["followedListHtml"])

    comics = []

    for page in pages:
        curr_len = len(comics)
        comics.extend(map(lambda i: f"{i[0] + curr_len + 1}. {i[1][0]} - {i[1][1]}", enumerate(extractComic(page))))

    return "\n".join(comics)