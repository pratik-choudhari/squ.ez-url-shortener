import sqlite3
import random
import string
import re

# URL verification regex 
regex = r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"""

# check_same_thread=False to disable thread sync
conn = sqlite3.connect("url.db", check_same_thread=False)


def check_if_exists(id):
    query = f'''SELECT COUNT(*) FROM URLS WHERE ID="{id}";'''
    db_res = conn.execute(query)
    if [i[0] for i in db_res] == [0]:
        return False
    else:
        return True


def insert_data(id, og, value):
    query = f'''INSERT INTO URLS (ID, ORIGINAL, VISITS) VALUES ("{str(id)}", "{str(og)}", {int(value)});'''
    db_res = conn.execute(query)
    conn.commit()
    if not db_res:
        return False
    else:
        return True


def get_original_url(id):
    query = f'''SELECT ORIGINAL FROM URLS WHERE ID="{str(id)}";'''
    db_res = conn.execute(query)
    url = [i[0] for i in db_res]
    if url:
        return url[0]
    else:
        return False

def get_valid_combination(url: str)-> str:
    res = re.findall(regex, url)
    url = url.replace("https://www", "")
    url = url.replace("http://www", "")
    url = url.replace("https://", "")
    url = url.replace("http://", "")
    url = url.replace("www.", "")
    data = False
    if res:
        while 1:
            shrt = ''.join(random.choice(string.ascii_letters) for _ in range(8))
            if not check_if_exists(shrt):
                if not insert_data(shrt, url, 0):
                    return False
                else:
                    data = "".join(["localhost/", shrt])
                    break
    return data
