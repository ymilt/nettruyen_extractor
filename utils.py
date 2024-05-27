import string

ALPHABET = {'à','á','ã','ả','ạ','ă','ằ','ắ','ẳ','ẵ','ặ','â','ầ','ấ','ẩ','ẫ','ậ','è','é','ẻ','ẽ','ẹ','ê','ề','ế','ể','ễ','ệ','đ','ù','ú','ủ','ũ','ụ','ư','ừ','ứ','ử','ữ','ự','ò','ó','ỏ','õ','ọ','ô','ồ','ố','ổ','ỗ','ộ','ơ','ờ','ớ','ở','ỡ','ợ','ì','í','ỉ','ĩ','ị','ä','ë','ï','î','ö','ü','û','ñ','ç','ý','ỳ','ỹ','ỵ','ỷ'}
for x in list(ALPHABET):
    ALPHABET.add(x.upper())
ALPHABET = ALPHABET.union(set(string.printable[:-5]) - set(r"\/:*?\"<>|"))

def filter(name, set = ALPHABET):
    out = ""
    for c in name:
        out += c if c in set else "_"
    return out