import requests
from bs4 import BeautifulSoup
from urllib import parse
import codecs
import json
import pandas as pd
import csv
import time, random
csvFile = codecs.open('./OutputFile.csv','w','utf-8-sig')
csvWriter = csv.writer(csvFile)

FieldName = ['職稱','更新時間','公司名稱','職務類別','工作待遇','上班地點','地址','管理責任','出差外派', \
                            '上班時段','休假制度','可上班日','需求人數','接受身分','工作經歷','學歷要求','科系要求',    \
                            '語文條件','擅長工具','工作技能','其他條件']
csvWriter.writerow(FieldName)
#coding=utf-8
# 查詢之網頁路徑
url = 'https://www.104.com.tw/jobs/search/'
# 導入正規的 headers
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
headers = {'User-Agent': useragent}
# s = b'\xe4\xb8\xad\xe6\x96\x87'
# b = s.decode()
# print(b)

# '資料分析師'
job_name = input('請輸入關鍵字:')
job_name = parse.quote(job_name)
page_count = int(input('搜尋頁數:'))
#page_count = 10
#print(job_name)
for page in range(page_count):
    url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword=%s&order=1&asc=0&page=%d&mode=s' % (job_name, page)
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup)
    action_span = soup.findAll('article', class_="b-block--top-bord job-list-item b-clearfix js-job-item")
    for article_list in action_span:
        # print('-----------------------------------')
        article_title = article_list['data-job-name']
        article_url = 'https:'+article_list.a['href']
        article_com = article_list['data-cust-name']
        # print(article_title)
        # print(article_url)
        # print(article_com)
        # ---內文處理---
        stag = article_url.split('/')[4].split('?')[0]
        article_content_url = 'https://www.104.com.tw/job/ajax/content/' + stag
        # print(article_content_url)
        article_content_res = requests.get(article_content_url, headers=headers)
        article_content_soup = BeautifulSoup(article_content_res.text, 'html.parser')
        json_string = str(article_content_soup)
        js = json.loads(json_string)
        # print(js)
        # for each_element in js['data']['jobDetail']['jobCategory']:
        #     print(each_element)
        #print('職稱:' , js['data']['header']['jobName'])
        jobName = js['data']['header']['jobName']
        #print('更新時間:' , js['data']['header']['appearDate'])
        appearDate = js['data']['header']['appearDate']
        #print('公司名稱:' , js['data']['header']['custName'])
        custName = js['data']['header']['custName']
        #print('職務類別:' , js['data']['jobDetail']['jobCategory'][0]['description'])
        description = js['data']['jobDetail']['jobCategory'][0]['description']
        #print('工作待遇:' , js['data']['jobDetail']['salary'])
        salary = js['data']['jobDetail']['salary']
        # print('工作性質:x')
        # print('上班地點:' , js['data']['jobDetail']['addressRegion'])
        addressRegion = js['data']['jobDetail']['addressRegion']
        address = js['data']['jobDetail']['addressDetail']
        #print('管理責任:' , js['data']['jobDetail']['manageResp'])
        manageResp = js['data']['jobDetail']['manageResp']
        #print('出差外派:' , js['data']['jobDetail']['businessTrip'])
        businessTrip = js['data']['jobDetail']['businessTrip']
        #print('上班時段:' , js['data']['jobDetail']['workPeriod'])
        workPeriod = js['data']['jobDetail']['workPeriod']
        #print('休假制度:' , js['data']['jobDetail']['vacationPolicy'])
        vacationPolicy = js['data']['jobDetail']['vacationPolicy']
        #print('可上班日:' , js['data']['jobDetail']['startWorkingDay'])
        startWorkingDay = js['data']['jobDetail']['startWorkingDay']
        #print('需求人數:' , js['data']['jobDetail']['needEmp'])
        needEmp = js['data']['jobDetail']['needEmp']
        # print('----條件要求----')
        #print('接受身份:' , js['data']['condition']['acceptRole']['role'][0]['description'])
        description = js['data']['condition']['acceptRole']['role'][0]['description']
        #print('工作經歷:' , js['data']['condition']['workExp'])
        workExp = js['data']['condition']['workExp']
        #print('學歷要求:' , js['data']['condition']['edu'])
        edu = js['data']['condition']['edu']
        # 科系要求
        major = ''
        for ma in js['data']['condition']['major']:
            major = ma
        if major == '':
            major = '不拘'
        # 語文條件
        languages = ''
        for lan in js['data']['condition']['language']:
            languages += lan['language'] + ":" + lan['ability'] +'\n'
        if languages == '':
            languages = '不拘'
        # 擅長工具
        specialty = ''
        for spec in js['data']['condition']['specialty']:
            specialty += spec['description'] + '\n'
        if specialty == '':
            specialty = '不拘'
        # 工作技能
        skills = ''
        for sk in js['data']['condition']['skill']:
            skills += sk['description'] + '\n'
        if skills == '':
            skills = '不拘'
        # 其他條件
        other = js['data']['condition']['other']
        rowData = [jobName,appearDate,custName,description,salary,addressRegion,address,manageResp,businessTrip, \
                   workPeriod,vacationPolicy,startWorkingDay,needEmp,description,workExp,edu,major,languages,specialty,\
                   skills,other]
        csvWriter.writerow(rowData)
       # time.sleep(random.randint(3,5))
csvFile.close()
print("搜尋完成，請至OutputFile.csv察看結果")
