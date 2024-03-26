import requests
from bs4 import BeautifulSoup

with open("index.html") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")

cookies = {
    'dle_user_taken': '1',
    '_ym_uid': '1710714161402410980',
    '_ym_d': '1710714161',
    'dle_user_id': '929415',
    'dle_password': 'f74fe3fcea2e3b01515b2b914eccb5fb',
    'dle_newpm': '0',
    'dle_user_token': '66f5d150fcbc25079bf9295da0219654',
    'newest_tab': '1',
    'rzk_theme': 'night',
    '_clck': '1hc6yta%7C2%7Cfkd%7C0%7C1537',
    '_ym_isad': '2',
    'PHPSESSID': '5lekglp9vfgvm4oe6316gij83v',
    '_ym_visorc': 'b',
    '_clsk': '1kwlboe%7C1711387086846%7C2%7C0%7Ca.clarity.ms%2Fcollect',
    'PHPSESSID': '8o8o3ibcm50nd5r7gjup63mfev',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'dle_user_taken=1; _ym_uid=1710714161402410980; _ym_d=1710714161; dle_user_id=929415; dle_password=f74fe3fcea2e3b01515b2b914eccb5fb; dle_newpm=0; dle_user_token=66f5d150fcbc25079bf9295da0219654; newest_tab=1; rzk_theme=night; _clck=1hc6yta%7C2%7Cfkd%7C0%7C1537; _ym_isad=2; PHPSESSID=5lekglp9vfgvm4oe6316gij83v; _ym_visorc=b; _clsk=1kwlboe%7C1711387086846%7C2%7C0%7Ca.clarity.ms%2Fcollect; PHPSESSID=8o8o3ibcm50nd5r7gjup63mfev',
    'Referer': 'https://hdrezka.me/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="123", "Not:A-Brand";v="8"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

response = requests.get('https://hdrezka.me/films/fiction/2259-interstellar-2014.html',
                        cookies=cookies, headers=headers)

print(response.text)
