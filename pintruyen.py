from curl_cffi import requests
from hashlib import md5
from typing import Literal
from urllib.parse import quote
import ujson

_type = type

class type:

    @staticmethod
    def jsondec(func):
        def wrapper(*args, **kwargs) -> dict:
            return ujson.loads(func(*args, **kwargs))
        return wrapper  
    
    @staticmethod
    def comiclist(func):
        def wrapper(*args, **kwargs) -> tuple:
            return tuple(map(Components.Comic, func(*args, **kwargs)))
        return wrapper

    @staticmethod
    def comic(func):
        def wrapper(*args, **kwargs):
            return Components.Comic(func(*args, **kwargs))
        return wrapper

    @staticmethod
    def chapter(func):
        def wrapper(*args, **kwargs):
            return Components.Chapter(func(*args, **kwargs))
        return wrapper

    @staticmethod
    def comments(func):
        def wrapper(*args, **kwargs):
            return Components.Comment.Page(func(*args, **kwargs))
        return wrapper

def toInt(num: str):
    try:
        return int(num.replace(",", ""))
    except:
        return num


class Notification:

    class Follow:

        def __init__(self, info: dict):

            self.success = info["success"]
            self.isFollowed = info["isFollowed"]
            self.message = info["message"]
            self.followCount = toInt(info["followCount"])

class Sort:

    TOP_ALL = 10
    TOP_MONTH = 11
    TOP_WEEK = 12
    TOP_DAY = 13
    LATEST = 15
    TOP_FOLLOWS = 19
    FOLLOWS = 20
    COMMENTS = 25
    CHAPTERS = 30

class Status:

    FINISHED = 2
    ON_GOING = 1
    ALL = -1

class API:

    KEY = "ec2cd8946e4b4b5792189afbccbab609"
    VERSION = 112

    HOST = "pintruyen.com"
    TYPE = "/api/"

    AUTH_URL = f"https://www.{HOST}/api/auth/token"
    URL = f"https://www.{HOST}{TYPE}"
    FOLLOW_URL = f"https://{HOST}{TYPE}"

    sess = requests.Session()

    class Sign:
        def new(param: str):
            return md5((API.KEY + param).encode()).hexdigest()
        
        def dullUrl(x):
            return x

        def URL(param: str, use_follow_url: bool = False):
            return f"{API.FOLLOW_URL if use_follow_url else API.URL}{param}{'?' if '?' not in param else '&'}sign={API.Sign.new(param)}"
    
    @type.jsondec
    def get(param: str, *args, urlSigner = Sign.URL, useFollowUrl = False, impersonate = "chrome124", **kwargs):
        return API.sess.get(urlSigner(param, useFollowUrl), impersonate=impersonate, timeout=10, *args, **kwargs).text
        
    @type.jsondec
    def post(*args, impersonate = "chrome124", **kwargs):
        return API.sess.post(*args, impersonate=impersonate, timeout=10, **kwargs).text
    
    class Account:

        @staticmethod
        def login(username: str, password: str):
            
            data = f"grant_type=password&username={quote(username)}&password={quote(password)}"

            headers = {
                "accept": "application/json, text/plain, */*",
                "user-agent": "Mozilla/5.0 (Linux; Android 13; sdk_gphone_x86_64 Build/TE1A.220922.028; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.71 Mobile Safari/537.36",
                "origin": "http://localhost",
                "x-requested-with": "com.pintruyen",
                "sec-fetch-site": "cross-site",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "http://localhost/",
                "accept-encoding": "gzip, deflate",
                "accept-language": "en-US,en;q=0.9",
                "content-type": "application/x-www-form-urlencoded",
				"sign": API.Sign.new(username + password)
            }

            return API.post("https://www.pintruyen.com/api/auth/token", data=data, headers=headers)
        
        @staticmethod
        def user(token: str, token_type: str):
            return API.get("auth/account", headers={
                "authorization": f"{token_type} {token}"
            })

    class Comic:

        @type.comiclist
        def search(keyword: str, page: int = 1):
            return API.get(f"comic/search?keyword={quote(keyword)}&page={page}")
        
        @type.comiclist
        def popular():
            return API.get("comic/popular")
        
        @type.comiclist
        def latest(page: int = 1):
            return API.get(f"comic/list?page={page}")
        
        
        def getPageAdv(
                page: int = 1, *, 
                position = None, 
                genres: list[int] = None, 
                not_genres: list[int] = None, 
                gender: Literal["Boy"] | Literal["Girl"] = None, 
                status: int = None, 
                minchapter: int = None, 
                sort: int = None
            ):
            M = f"comic/listadv?page={page}"
            if genres:
                M += f"&genres={','.join(map(str, genres))}"
            if not_genres:
                M += f"&notgenres={','.join(map(str, genres))}"
            if gender:
                M += f"&gender={gender}"
            if status:
                M += f"&status={status}"
            if position:
                M += f"&position={position}"
            if minchapter:
                M += f"&minchapter={minchapter}"
            if sort:
                M += f"&sort={sort}"
            return API.get(M)

        @type.comic
        def getComicDetail(comic_id: int):
            return API.get(f"comic/detail/{comic_id}")
        
        @type.comic
        def getComicDownload(comic_id: int):
            return API.get(f"comic/download/{comic_id}")
        
        @type.chapter
        def getChapterDetail(chapter_id: int):
            return API.get(f"chapter/detail/{chapter_id}")

        @type.chapter
        def getChapterDownload(chapter_id: int):
            return API.get(f"chapter/download/{chapter_id}")

        def getGenre(genre_id: int):
            return API.get(f"genre/get/{genre_id}")

        def getGenres():
            return API.get("genre/list")

        @type.comments
        def getComments(comic_id: int, page: int = 1):
            return API.get(f"comment/list?comicid={comic_id}&page={page}")

        @type.comiclist
        def getFollows(userguid: str, page: int = 1):
            return API.get(f"follow/list?page={page}&userguid={userguid}", useFollowUrl=True)

        def isFollowed(userguid: str, comic_id: int) -> bool:
            return API.get(f"follow/isfollowedcomic?comicid={comic_id}&userguid={userguid}", useFollowUrl=True)

        def isFollowedChapter(userguid: str, chapter_id: int) -> bool:
            return API.get(f"follow/isfollowedchapter?chapterid={chapter_id}&userguid={userguid}", useFollowUrl=True)

        def followComic(userguid: str, comic_id: int):
            return Notification.Follow(API.get(f"follow/follow?comicid={comic_id}&userguid={userguid}"))

        def initApp(userguid: str = "", token: str = "", platforms: str = "android,cordova,capacitor,desktop,hybrid") -> bool:
            return API.get(f"notification/initapp?platforms={platforms}&version={API.VERSION}&token={token}&userGuid={userguid}", useFollowUrl=True)
        
        def markAsRead(userguid: str, comic_id: int, chapter_ids: str) -> bool:
            return API.get(f"follow/markasread?comicid={comic_id}&userguid={userguid}&chapterids={chapter_ids}", useFollowUrl=True)

    def registerToken(userguid: str, token: str) -> bool:
        return API.get(f"subscribe/registertoken?token={token}&userguid={userguid}", useFollowUrl=True)

    def deleteToken(token: str) -> bool:
        " Currently non-functionable "
        return API.get(f"subscribe/deletetoken?token={token}", useFollowUrl=True)

    def receivedMessage(message):
        " Currently non-functionable "
        return requests.get(message)

    def getNotifications(userguid: str, token: str, page: int = 1):
        return API.get(f"notification/list?page={page}&userguid={userguid}&token={token}")


API.sess.headers = {
    "accept": "application/json, text/plain, */*",
    "user-agent": "Mozilla/5.0 (Linux; Android 13; sdk_gphone_x86_64 Build/TE1A.220922.028; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.71 Mobile Safari/537.36",
    "origin": "http://localhost",
    "x-requested-with": "com.pintruyen",
    "sec-fetch-site": "cross-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "http://localhost/",
    "accept-encoding": "gzip, deflate",
    "accept-language": "en-US,en;q=0.9",
}


class Components:

    Genres = {"Action":1,"Adult":2,"Adventure":3,"Anime":4,"Chuy\u1ec3n Sinh":5,"Comedy":6,"Comic":7,"Cooking":8,"C\u1ed5 \u0110\u1ea1i":9,"Doujinshi":10,"Drama":11,"\u0110am M\u1ef9":12,"Fantasy":14,"Gender Bender":15,"Harem":16,"Historical":17,"Horror":18,"Josei":20,"Live action":21,"Manga":23,"Manhua":24,"Manhwa":25,"Martial Arts":26,"Mature":27,"Mecha":28,"Mystery":30,"Ng\u00f4n T\u00ecnh":32,"One shot":33,"Psychological":34,"Romance":35,"School Life":36,"Sci-fi":37,"Seinen":38,"Shoujo":39,"Shoujo Ai":40,"Shounen":41,"Shounen Ai":42,"Slice of Life":43,"Sports":47,"Supernatural":48,"Thi\u1ebfu Nhi":50,"Tragedy":51,"Trinh Th\u00e1m":52,"Truy\u1ec7n M\u00e0u":53,"Truy\u1ec7n scan":54,"Vi\u1ec7t Nam":55,"Webtoon":56,"Xuy\u00ean Kh\u00f4ng":57}

    class Comment:

        def __init__(self, info: dict):

            self.fullName = info["fullName"]
            self.content = info["content"]
            self.truncatedContent = info["truncatedContent"]
            self.timeAgo = info["timeAgo"]
            self.avatar = info["avatar"]
            self.memberText = info["memberText"]
            self.memberType = info["memberType"]
            self.childComments = tuple(map(Components.Comment, info["childComments"]))

        class Page:

            def __init__(self, info: dict):

                self.comicId = info["comicId"]
                self.comicName = info["comicName"]
                self.commentCount = info["commentCount"]
                self.comments = tuple(map(Components.Comment, info["comments"]))

    class Chapter:

        class Comic:

            def __init__(self, info: dict):

                self.id = info["comicId"]
                self.name = info["comicName"]
                self.image = info["comicImage"]
                self.commentCount = toInt(info["commentCount"])

        class ShortCut:

            def __init__(self, info: dict):
                
                self.id, self.number = None, None

                if info:
                    self.id = info["id"]
                    self.number = info["number"]

        def __init__(self, info: dict):
            
            self.id = info["id"]
            self.number = info["number"]
            self.title = info["title"].strip()
            self.time = info["time"].strip()
            self.viewCount = toInt(info["viewCount"])
            self.isVip = info["isVip"]

            if "encrypt" in info: # Alternative for `verbose`

                self.comic = Components.Chapter.Comic(info)
                self.next = Components.Chapter.ShortCut(info["next"])
                self.prev = Components.Chapter.ShortCut(info["prev"])
                self.encrypt = info["encrypt"]
                self.webURL = info["webUrl"]

                self.images = [None] * len(info["images"])
                for img in info["images"]:
                    self.images[img["index"]] = img["imageUrl"]
                self.images = tuple(self.images)

        def json(self):

            return {
                "id": self.id,
                "num": self.number,
                "img": self.images
            }
                
    class Comic:

        def __init__(self, info: dict):

            self.id = info["id"]
            self.name = info["name"]
            self.imageURL = info["imageUrl"]
            self.viewCount = toInt(info["viewCount"])
            self.commentCount = toInt(info["commentCount"])
            self.followCount = toInt(info["followCount"])
            self.chapters = tuple(map(Components.Chapter, info["chapters"]))

            self.lastViewChapter = info.pop("lastViewChapter", None)
            if self.lastViewChapter:
                self.lastViewChapter = Components.Chapter(self.lastViewChapter)

            self.verbose = "otherName" in info

            if self.verbose:

                self.otherName = info["otherName"]
                self.modifiedDate = info["modifiedDate"]
                self.description = info["description"]
                self.author = info["author"]
                self.status = info["status"]
                self.genres = tuple(map(lambda x: x["name"], info["genres"]))

        def json(self):
            try:
                chaps = []
                for chap in (self.chapters if self.verbose else API.Comic.getComicDetail(self.id).chapters):
                    try:
                        chapdata = API.Comic.getChapterDetail(chap.id).json()
                    except:
                        chapdata = {"id": chap.id, "num": chap.number}
                    chaps.append(chapdata)
            except:
                chaps = []
            return {
                "name": self.name,
                "id": self.id,
                "img": self.imageURL,
                "chaps": chaps
            }


class UserInfo:

    @staticmethod
    def fromToken(token: str, type: str, expire: int):
        user = UserInfo()

        user.token, user.type, user.expire = token, type, expire

        userdata = API.Account.user(token, type)

        user.id = userdata["id"]
        user.username = userdata["userName"]
        user.firstname = userdata["firstName"]
        user.lastname = userdata["lastName"]
        user.email = userdata["email"]
        user.guid = userdata["guid"]

        return user

    @staticmethod
    def fromCredential(email: str, password: str):
        data = API.Account.login(email, password)

        return UserInfo.fromToken(data["access_token"], data["token_type"], data["expires_in"])

    def __init__(self):
        self.token = ""
        self.type = ""
        self.expire = -1

        self.id = -1
        self.username = ""
        self.firstname = ""
        self.lastname = ""
        self.email = ""
        self.guid = ""

    def regisToken(self) -> bool:
        return API.registerToken(self.guid, self.token)
    
    def delToken(self) -> bool:
        return API.deleteToken(self.token)


class Session:

    def __init__(self, user: UserInfo):
        self.user = user

    def getFollows(self, page: int = 1):
        return API.Comic.getFollows(self.user.guid, page)
    
    def isFollowed(self, comic_id: int) -> bool:
        return API.Comic.isFollowed(self.user.guid, comic_id)
    
    def isFollowedChapter(self, chapter_id: int) -> bool:
        return API.Comic.isFollowedChapter(self.user.guid, chapter_id)
    
    def followComic(self, comic_id: int):
        return API.Comic.followComic(self.user.guid, comic_id)
    
    def initApp(self) -> bool:
        return API.Comic.initApp(self.user.guid, self.user.token)
    
    def markAsRead(self, comic_id: int, chapter_ids: list|str) -> bool:
        if not isinstance(chapter_ids, str):
            chapter_ids = ",".join(map(str, chapter_ids))
        return API.Comic.markAsRead(self.user.guid, comic_id, chapter_ids)