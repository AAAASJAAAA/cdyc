#! /usr/local/python3/bin/python3.6
#coding=utf-8
import datetime
import logging
import os
import sys
import pymysql
import requests
from lxml import etree

def script_path():
    path = os.path.realpath(sys.argv[0])
    if os.path.isfile(path):
        path = os.path.dirname(path)
    return os.path.abspath(path)
def logg(log):

    log_path = os.path.join(script_path(), 'logs')
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    logger = logging.getLogger(__name__)
    time = datetime.datetime.now().strftime('%Y-%m-%d')
    outlog = 'lishi' + str(time) + '.log'
    file_handler = logging.FileHandler(log_path+'//'+outlog,encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.warning(log)

def into(rq,sj,Rate,mz,Value_type,Data_source,Web,execution_time):
    try:
        conn = pymysql.connect(host='127.0.0.1', user='root', password='密码', database='cdyc', charset='utf8')
        cursor = conn.cursor()
        sql = "insert into tb_data (date,value,rate,name,valuetype,datasource,web,execution_time) values ('" + rq + "','" + sj + "','" + Rate + "','" + mz.replace('*','') + "','" + Value_type + "','" + Data_source + "','" + Web + "','" + execution_time + "')"
        # print(sql)
        cursor.execute(sql)
        print('成功插入', cursor.rowcount, '条数据')
        conn.commit()
        cursor.close()
    except Exception as e:
        logg(e)
        print(e)

# 获取表格数据
def data(url,name,time):
    while True:  # 如果requests 异常 重复执行
        try:
            s = requests.get(url)
            s_xpath = etree.HTML(s.text)
            tb1 = s_xpath.xpath('//*[@id="tbc_01"]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/*/text()')[-2]
            tb2 = s_xpath.xpath('//*[@id="tbc_02"]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/*/text()')[-2]
            tb3 = s_xpath.xpath('//*[@id="tbc_03"]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/*/text()')[-2]
            tb4 = s_xpath.xpath('//*[@id="tbc_04"]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/*/text()')[-2]
            tab_list = [int(tb1),int(tb2),int(tb3),int(tb4)]
            print('最大值',max(tab_list))

            for i in range(max(tab_list)):
                _url = 'http://www.ysindex.com/TabId/61/cat/'+str(url.split('=')[1])+'/curPage/'+str(i)+'/default.aspx'# 拼接 Url
                s1 = requests.get(_url)
                s1_xpath = etree.HTML(s1.text)
                for j in range(1,5):
                    zhishu = ''#判断周月指数
                    Rate = ''#判断周月指数
                    if j == 1:
                        zhishu = '周价格定基指数'
                        Rate = '2'
                    elif j ==2:
                        zhishu = '周价格环比指数'
                        Rate = '2'
                    elif j == 3:
                        zhishu = '月价格定基指数'
                        Rate = '5'
                    elif j == 4:
                        zhishu = '月价格环比指数'
                        Rate = '5'
                    for i in range(2,12):
                        data = s1_xpath.xpath('//*[@id="tbc_0'+str(j)+'"]/div[1]/div[2]/div[2]/div[1]/div[1]/table/tr['+str(i)+']/td/text()')#获取表格数据
                        if data:
                            print(data[0],data[1],Rate,name,zhishu,'成都中药材指数网',url,time)
                            into(data[0],data[1],Rate,name,zhishu,'成都中药材指数网',url,time)#写入数据库
        except Exception as e:
            print(e)
            logg(log=str(e) + '获取数据异常')
            pass
        else:
            break



if __name__ == '__main__':
    url = 'http://www.ysindex.com'  # 主网页
    price_index = 'priceindex.aspx'  # 价格指数url
    get_url = requests.get(url + '/' + price_index)
    html_etree = etree.HTML(get_url.text)
    html_xpath = html_etree.xpath('//*[@id="menulist"]/div/div/div/a[1]/@href')  # 大类url
    html_xpath1 = html_etree.xpath('//*[@id="menulist"]/div/div/div/a[1]/text()')  # 大类name
    bigclass_url = []
    smclass_url = []
    for i in range(len(html_xpath)):
        bigclass_url.append(url + html_xpath[i])
        smclass_url.append([url + html_xpath[i], html_xpath1[i]])
    get_bclass = requests.get(bigclass_url[1])
    html_betree = etree.HTML(get_bclass.text)
    html_bxpath01 = html_betree.xpath('//*[@id="menulist"]/div/div/dl/dd/a/@href')  # 药材url
    html_bxpath02 = html_betree.xpath('//*[@id="menulist"]/div/div/dl/dd/a/text()')  # 药材name
    for k in range(len(html_bxpath01)):
        smclass_url.append([url + html_bxpath01[k], html_bxpath02[k]])
    for i in smclass_url:
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data(i[0],i[1],time)
