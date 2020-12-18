import sqlite3
import random
import string
import re

# domain name
domain = "https://squez-url-shortener.herokuapp.com/"

# URL verification regex 
regex = r"""(?i)\b((?:https?://|www\d{0,3}[.]{0, 1}|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"""

# check_same_thread=False to disable thread sync
conn = sqlite3.connect("url.db", check_same_thread=False)


def check_if_exists(id: str, flag: bool):
    """
    returns true if record exists
    params:
        id: data to check in db
        flag: True if shortened URL, else False
    returns:
        True if record exists else False 
    """
    if flag:
        query = f'''SELECT COUNT(*) FROM URLS WHERE ID="{id}";'''
        db_res = conn.execute(query)
        if [i[0] for i in db_res] == [0]:
            return False
        else:
            return True
    else:
        query = f'''SELECT COUNT(*) FROM URLS WHERE ORIGINAL="{id}";'''
        db_res = conn.execute(query)
        if [i[0] for i in db_res] == [0]:
            return False
        else:
            return True


def insert_data(id: str, og: str, value: int):
    """
    Insert data in db
    Params:
        id: short url(primary key)
        og: original url
        value: number of visit
    returns:
        True if successful else False
    """
    query = f'''INSERT INTO URLS (ID, ORIGINAL, VISITS) VALUES ("{str(id)}", "{str(og)}", {int(value)});'''
    db_res = conn.execute(query)
    conn.commit()
    if not db_res:
        return False
    else:
        return True


def get_original_url(id: str, flag: bool):
    """
    returns record data if exists
    params:
        id: shortened or original url
        flag: True for shortened id else False
    returns:
        False if data doesn't exist else return data
    """
    if flag:
        query = f'''SELECT ORIGINAL FROM URLS WHERE ID="{str(id)}";'''
        db_res = conn.execute(query)
        url = [i[0] for i in db_res]
        if url:
            return url[0]
        else:
            return False
    else:
        query = f'''SELECT ID FROM URLS WHERE ORIGINAL="{str(id)}";'''
        db_res = conn.execute(query)
        url = [i[0] for i in db_res]
        if url:
            return url[0]
        else:
            return False


def get_valid_combination(url: str)-> str:
    """
    finds and returns shortened URL
    params:
        url: original url
    returns:
        False if operation failed else return whole shortened link
    """
    res = re.findall(regex, url)
    url = re.sub(r"^(http://|https://){0,1}(www.|ww.|w.){0,1}", "", url)
    # url = url.replace("https://www.", "")
    # url = url.replace("http://www.", "")
    # url = url.replace("https://", "")
    # url = url.replace("http://", "")
    # url = url.replace("www.", "")
    data = False
    if res:
        if not check_if_exists(url, False):
            while 1:
                shrt = ''.join(random.choice(string.ascii_letters) for _ in range(8))
                if not check_if_exists(shrt, True):
                    if not insert_data(shrt, url, 0):
                        return False
                    else:
                        data = "".join([domain, shrt])
                        break
        else:
            shrt = get_original_url(url, False)
            data = "".join([domain, shrt])
    return data
