import requests
from bs4 import BeautifulSoup as BS

urls = {'main': 'https://www.mos.ru/',
        'auth': 'https://login.mos.ru/sps/login/methods/password',
        'dir': 'https://mrko.mos.ru/dnevnik/services/index.php'}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'ru,en;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'bnr=false; blu=eyJsb2dpbiI6ImhlcmV3MjZAZ21haWwuY29tIiwibmFtZSI6ItCX0LTRgNCw0LLRgdGC0LLRg9C50YLQtSwg0KLQuNC80L7RhNC10LkiLCJtZXRob2QiOiJwYXNzd29yZCJ9; fm=eyJtZXRob2RzIjpbInBhc3N3b3JkIiwieDUwOSIsImV4dGVybmFsSWRwcyJdLCJwYXJhbXMiOnsiY2hhbGxlbmdlIjoiV3J2NXRVSWd5WS9uc1gzSHNCbFEiLCJmZWRQb2ludHMiOiJ5YW5kZXg6eWFuZGV4XzF8c2JyZjpzYnJmXzF8Z29vZ2xlOmdvb2dsZV8xfHZrOnZrXzF8ZmFjZWJvb2s6ZmFjZWJvb2tfMXxlc2lhOmVzaWFfMXxvazpva18xIn19; history=eyJtZXRob2QiOiJwYXNzd29yZCJ9; bfp=b85a4d3f8c249b8bacbd55c826a013ab; blg=ru; bud=6A9rePpIo13lc_ZLHGlsG7ozs2MN4iAnwFV7PSG9grzrqYZ_ydKv63hv_RUG3uEot77IF6MUKLvPf4dG_QWfLlLGrDCsGo17vF8t7lgK0Mdyg4QalWLiYDuoP0GKilyuSafKWFQXl5kmwwoXB77e; origin=53w5fwZVaZiNYy4QYHZp|%2Fsps%2Foauth%2Fae%3Fscope%3Dprofile%2Bopenid%2Bcontacts%26response_type%3Dcode%26redirect_uri%3Dhttps%3A%2F%2Fwww.mos.ru%2Fapi%2Facs%2Fv1%2Flogin%2Fsatisfy%26client_id%3D53w5fwZVaZiNYy4QYHZp; oauth_az=-nV6FKbe0fXG3D1KC9QTk9mw57J5Dio8ticnHsXDte0fLOKFS1gqCOuBVJgzZfQwGlpHVprnvnnxOdgQmocD3lZzIHsb6_CVXma04yYeIJc; lstate=fP-9C662peCfNPeO59Nk-LhyMyeEfUugBNgvttnLXAfDNYU8_0cWJVEnev6r3Ts1ZrEuNoHUE3sG_jgQS6uVtnF_Z2bLYd5FI21A0_G4RmiMUMcLQmWV60WjVuTo8HN3A_Vz749ArlHcmbRwl2rRQIQLPCkOREb-Du4mY3VazF4K5f_qMnUeDXy43QpzH-p7ua-BO7LVZgNN6SSolCtHAiANerGAshnuW9_W9sux95UH-Pa6Bf0ZPIYk96JhQ72cFLOttzEY__2WZqAh_shnc2jUhhGN0VtMUx-AvDuz6Zy4T5DzDscm5eoiBJyn4uaf3ahYgcEHWSnghFTHbL0cWM2xHn-aEPw_a4xotbzAPcv09Izlf3OeXSth4-N0VEKpfqNaZ3MRHSZHISHrDrnkyB9Pp7nxp9YMaH5rbszFFJICF0IUFbkp0wzf_vDp_jh3YrfZ4z6IA0DTd33Pa37rubmf9fb08s0Qrx5SM4HOKN5PZkS697f8j2RYwNJlQamCj2siwjHsMekPqrmLp7V8Vsgp9oqwWY-qzlamqaAe-00TdMBzi-21gKCuKDbuuyFr|MTU4NjAxMzYxNg|U0gxQVMxMjhDQkM|oBETI3aD6W_IIzZbsFDnbg|-1MAXkVobr5v5x4pPO65KO10v70; _ym_d=1576329390; _ym_uid=1576329390797819326; mos_id=Cg8qAl304L5uxThHpqtvAgA=; _ym_visorc_26555085=w; _ym_visorc_14112952=b; _ym_visorc_32628510=w; _ym_isad=2; session-cookie=1602a5fb9c7c08cd277bbc2e80267f93054d476a6e0ad3698c9f0a7b1e3f76f6e466dcffa188cb5d013401ec3c966a2f; _ym_visorc_53480143=w; csrf-token-name=csrftoken_w; Ltpaexpires=1586013439; csrf-token-value=1602a6fa2fbae014c14e631323bb0df86af3ea1a934f5f34c1e8afc51e48d818b3a750839e66c9a7',
    'Host': 'login.mos.ru',
    'Referer': 'https://www.mos.ru/services/catalog/popular/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 YaBrowser/20.3.2.238 Yowser/2.5 Safari/537.36}'}

with requests.Session() as session:
    # session.headers = headers

    r = session.get(urls['dir'])
    # session.headers = r.headers

    print(r.text)


def diary():
    session = requests.Session()
    headers = {'Referer': 'https://www.mos.ru/pgu/ru/application/dogm/journal/'}
    auth_url = "https://mrko.mos.ru/dnevnik/services/index.php"
    auth_req = session.get(auth_url, headers=headers, params={"login": 'herew26@gmail.com', "password": 'VYrixCH3F7CXhyi'}, allow_redirects=False)
    print(auth_req.text)
