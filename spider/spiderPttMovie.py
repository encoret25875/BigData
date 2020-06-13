import requests
from bs4 import BeautifulSoup
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 ' \
            'Safari/537.36 '
headers = {'User-Agent': useragent}
url = "https://www.ptt.cc/bbs/movie/index.html"
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
iInput = int(input('請輸入要查詢幾頁:'))
for i in range(iInput):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    title = soup.select('div[class="title"] a')
    # print(title)
    for t in title:
        print('--------')
        try:
            print(t.text)
            print('https://www.ptt.cc' + t['href'])

        except:
            print(t)

    last_page_url = 'https://www.ptt.cc' + soup.select('a[class="btn wide"]')[1]['href']
    url = last_page_url
