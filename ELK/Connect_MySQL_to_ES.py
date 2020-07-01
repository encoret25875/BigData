import MySQLdb
from elasticsearch import Elasticsearch
import requests, json, pandas
import pandas as pd
import time
import datetime
start = time.time() # 計算時間

# MySQL連線資訊
db = MySQLdb.connect(
    host=[MySQL_IP],
    user=[帳號],
    passwd='[密碼],
    db=[資料庫名稱],
    port=[port],
    charset=[文字編碼])

cursor = db.cursor()  # 建立游標

# 測試ES連線是否正常
url = 'http://localhost:9200/'
print(requests.get(url), ' ======>    Server Connected')

# 建立ES連線
es = Elasticsearch('http://localhost:9200/')
print('ES object : ', es)

# 抓取MySQL資料
try:
    sql_str_data = 'SELECT * FROM 資料庫名稱.資料表名稱'
    df = pd.read_sql(sql=sql_str_data, con=db)
    # df2 = df.iloc[0:2, :] # 取前兩row測試
    # print(df2)
    
except Exception as e:
    print(e)

## 將 Datarframe 轉 dict
doc = df.to_dict(orient="records")

# 顯示前10筆
# for i in range(0,10):
#     print(doc[i])

# 測試塞資料用
# doc = {
#     'author': 'Balao',
#     'text': 'oookkoo1oo',
#     'timestamp': datetime.datetime.now()
#     }

# 塞資料給es
for i in range(0,10):
    es.create(index='test01-index', id = i, body=doc[i])

end = time.time() # 計算時間
print(end - start)