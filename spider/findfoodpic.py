import threading
import time
import requests
from bs4 import BeautifulSoup
import os
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 ' \
            'Safari/537.36 '
headers = {'User-Agent': useragent}
threads = []
proxies = {
    "http": "14.140.131.82:3128"
}
os.makedirs('./img/',exist_ok=True)


def recipe_thread(thread_num, start_num, end_num):
    for page in range(start_num, end_num):
        # 抓食譜文章
        url = 'https://icook.tw/recipes/popular?page=%d' % page
        res = requests.get(url, headers=headers, proxies=proxies)
        soup = BeautifulSoup(res.text, 'html.parser')
        action_span = soup.findAll('a', class_="browse-recipe-touch-link")
        print('thread_num:', thread_num, '此頁食譜數量:', action_span.__len__(),' ',url)
        if action_span.__len__() == 0:
            print('thread_num:', thread_num, ', \033[0;32;40m此頁無文章\033[0m')
        for action in action_span:
            try:
                foodname = action['aria-label'].lstrip('前往').rstrip('食譜')
                # 取得食譜連結
                foodurl = 'https://icook.tw' + action['href']
                # 進入食譜的url處理
                food_res = requests.get(foodurl, headers=headers)
                food_soup = BeautifulSoup(food_res.text, 'html.parser')
                # 取得圖片url
                food_pic = food_soup.img['src']
                r = requests.get(food_pic)
                with open('./img/' + foodname + '.jpg', 'wb') as f:
                    f.write(r.content)
            except:
                pass
    print(start_num, '執行結束')


def main():
    # x  - > thread數 ,a -> thread工作範圍
    x = 8
    a = 1500
    for i in range(x):
        # 建立子執行緒
        threads.append(threading.Thread(target=recipe_thread, args=(i, i * a + 1, i * a + a)))
        # 執行該子執行緒
        threads[i].start()

    for i in range(x):
        threads[i].join()
    print("全部結束")


if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print("CPU Time: ", end - start)
