import codecs
import csv
import random
import threading
import time
import requests
from bs4 import BeautifulSoup

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 ' \
            'Safari/537.36 '
headers = {'User-Agent': useragent}
threads = []

icook_title = ["食譜名稱", "食譜連結", "食材", "圖片連結", "人數"]

proxies = {
    "http": "14.140.131.82:3128"
}


def recipe_thread(thread_num, start_num, end_num):
    csvFile = codecs.open('./iCook_' + str(start_num) + '.csv', 'w', encoding='utf-8-sig')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(icook_title)
    for page in range(start_num, end_num):
        # 抓食譜文章
        url = 'https://icook.tw/recipes/popular?page=%d' % page
        res = requests.get(url, headers=headers, proxies=proxies)
        soup = BeautifulSoup(res.text, 'html.parser')
        action_span = soup.findAll('a', class_="browse-recipe-touch-link")
        print('thread_num:', thread_num, '此頁食譜數量:', action_span.__len__(),' ',url)
        if action_span.__len__() == 0:
            print('thread_num:',thread_num,', \033[0;32;40m此頁無文章\033[0m')
        for action in action_span:
            try:
                # foodname 食物名稱 foodurl食譜連結 食材fooddict 圖片連結food_pic
                # 取得食譜名稱
                foodname = action['aria-label'].lstrip('前往').rstrip('食譜')

                # 取得食譜連結
                foodurl = 'https://icook.tw' + action['href']

                # 進入食譜的url 處理
                food_res = requests.get(foodurl, headers=headers)
                food_soup = BeautifulSoup(food_res.text, 'html.parser')
                food_span = food_soup.findAll('div', class_='ingredient')

                # 取得食材
                fooddict = {}
                for food in food_span:
                    a = food.text.strip()
                    Ingredients = a.split('\n')
                    Ingredients[1] = Ingredients[1].replace('約', '')
                    # print(Ingredients)
                    fooddict[Ingredients[0]] = Ingredients[1]
                # 取得圖片url
                food_pic = food_soup.img['src']

                # 份數 (null為空值)
                copies = 'null'
                food_span_test = food_soup.findAll('div', class_='servings-info info-block')
                # 確定有沒有份數欄位
                if food_span_test:
                    # 有份數欄位
                    food_span_num = food_soup.findAll('span', class_='num')
                    copies = food_span_num[0].text

                # 檔案處理開檔處理
                # print(foodname)
                rowData = [foodname, foodurl, fooddict, food_pic, copies]
                csvWriter.writerow(rowData)
            except:
                print("錯誤食譜編號:", foodname, foodurl)
        #time.sleep(random.randint(0, 3))
    csvFile.close()
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
