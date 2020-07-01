import MySQLdb
from elasticsearch import Elasticsearch
import requests, json, pandas
import pandas as pd
import time
import datetime
start = time.time() # �p��ɶ�

# MySQL�s�u��T
db = MySQLdb.connect(
    host=[MySQL_IP],
    user=[�b��],
    passwd='[�K�X],
    db=[��Ʈw�W��],
    port=[port],
    charset=[��r�s�X])

cursor = db.cursor()  # �إߴ��

# ����ES�s�u�O�_���`
url = 'http://localhost:9200/'
print(requests.get(url), ' ======>    Server Connected')

# �إ�ES�s�u
es = Elasticsearch('http://localhost:9200/')
print('ES object : ', es)

# ���MySQL���
try:
    sql_str_data = 'SELECT * FROM ��Ʈw�W��.��ƪ�W��'
    df = pd.read_sql(sql=sql_str_data, con=db)
    # df2 = df.iloc[0:2, :] # ���e��row����
    # print(df2)
    
except Exception as e:
    print(e)

## �N Datarframe �� dict
doc = df.to_dict(orient="records")

# ��ܫe10��
# for i in range(0,10):
#     print(doc[i])

# ���ն��ƥ�
# doc = {
#     'author': 'Balao',
#     'text': 'oookkoo1oo',
#     'timestamp': datetime.datetime.now()
#     }

# ���Ƶ�es
for i in range(0,10):
    es.create(index='test01-index', id = i, body=doc[i])

end = time.time() # �p��ɶ�
print(end - start)