#! /usr/local/python3/bin/python3.6
#coding=utf-8
import os
import requests
from lxml import etree
import threading
import pymysql
import logging
import datetime
import sys


url = 'http://www.ysindex.com'
_url = 'http://www.ysindex.com/priceindex.aspx'
type_value = ['周价格定基指数','周价格环比指数','月价格定基指数','月价格环比指数']
#-------------------日志写入--------------------
log = ''
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
    outlog = 'outlog' + str(time) + '.log'
    file_handler = logging.FileHandler(log_path+'//'+outlog,encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.warning(log)

#-------------------数据库写入---------------------
def into(rq,sj,Rate,mz,Value_type,Data_source,Web,execution_time):
    try:
        conn = pymysql.connect(host='127.0.0.1', user='root', password='密码', database='cdyc', charset='utf8')
        cursor = conn.cursor()
        sql = "insert into tb_data (date,value,rate,name,valuetype,datasource,web,execution_time,remarks) values ('" + rq + "','" + sj + "','" + Rate + "','" + mz.replace('*','') + "','" + Value_type + "','" + Data_source + "','" + Web + "','" + execution_time + "','')"
        print(sql)
        cursor.execute(sql)
        print('成功插入', cursor.rowcount, '条数据')
        conn.commit()
        cursor.close()
    except Exception as e:
        print(e)
        logg(log= str(e)+'数据库异常')



def subclass(subclass_data,execution_time,rate):

    for sub_name,sub_url in subclass_data:
        print(sub_name)
        while True:#如果requests 异常 重复执行
            try:
                sub_url1 = url + sub_url
                subclass_data = requests.get(sub_url1)
                # print(subclass_data)
                sub_xpath = etree.HTML(subclass_data.text)

                if rate == '2':
                    week_data0 = sub_xpath.xpath('//*[@id="tbc_01"]/div[1]/div[2]/div[2]/div[1]/div[1]/table/tr[2]/td/text()')
                    week_data1 = sub_xpath.xpath('//*[@id="tbc_02"]/div[1]/div[2]/div[2]/div[1]/div[1]/table/tr[2]/td/text()')
                    if week_data0:
                        into(str(week_data0[0]), str(week_data0[1]), rate, sub_name, str(type_value[2]), '成都中药材指数网',sub_url1, execution_time)
                    else:
                        week1_data0 = sub_xpath.xpath('//*[@id="tbc_01"]/div[1]/div[1]/div[2]/div[1]/div[1]/span/div[1]/div[1]/div[1]/div[1]/text()')[0].replace('发布日期：', '').replace(' ', '').replace('年', '-').replace('月', '-').replace('日','')
                        week1_data1 = sub_xpath.xpath('//*[@id="tbc_01"]/div[1]/div[1]/div[2]/div[1]/div[1]/span/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/text()')
                        if week1_data0 != '' and week1_data1:
                            into(str(week1_data0), str(week1_data1[0]), rate, sub_name, str(type_value[3]), '成都中药材指数网',sub_url1, execution_time)
                    if week_data1:
                        into(str(week_data1[0]), str(week_data1[1]), rate, sub_name, str(type_value[2]), '成都中药材指数网',sub_url1, execution_time)
                    else:
                        week1_data0 = sub_xpath.xpath('//*[@id="tbc_02"]/div[1]/div[1]/div[2]/div[1]/div[1]/span/div[1]/div[1]/div[1]/div[1]/text()')[0].replace('发布日期：', '').replace(' ', '').replace('年', '-').replace('月', '-').replace('日','')
                        week1_data1 = sub_xpath.xpath('//*[@id="tbc_02"]/div[1]/div[1]/div[2]/div[1]/div[1]/span/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/text()')
                        if week1_data0 != '' and week1_data1:
                            into(str(week1_data0), str(week1_data1[0]), rate, sub_name, str(type_value[3]), '成都中药材指数网', sub_url1,execution_time)
                elif rate == '5':
                    month_data0 = sub_xpath.xpath('//*[@id="tbc_03"]/div[1]/div[2]/div[2]/div[1]/div[1]/table/tr[2]/td/text()')
                    month_data1 = sub_xpath.xpath('//*[@id="tbc_04"]/div[1]/div[2]/div[2]/div[1]/div[1]/table/tr[2]/td/text()')

                    if month_data0:
                        into(str(month_data0[0]), str(month_data0[1]), rate, sub_name, str(type_value[2]), '成都中药材指数网',sub_url1, execution_time)
                    else:
                        month1_0 = sub_xpath.xpath('//*[@id="tbc_03"]/div[1]/div[1]/div[2]/div[1]/div[1]/span/div[1]/div[1]/div[1]/div[1]/text()')[0].replace('发布日期：','').replace(' ','').replace('年','-').replace('月','-').replace('日','')
                        month1_1 = sub_xpath.xpath('//*[@id="tbc_03"]/div[1]/div[1]/div[2]/div[1]/div[1]/span/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/text()')
                        if month1_0 != '' and month1_1:
                            into(str(month1_0), str(month1_1[0]), rate, sub_name, str(type_value[3]), '成都中药材指数网',sub_url1, execution_time)

                    if month_data1:
                        into(str(month_data1[0]), str(month_data1[1]), rate, sub_name, str(type_value[3]), '成都中药材指数网',sub_url1, execution_time)
                    else:
                        month1_0 = sub_xpath.xpath('//*[@id="tbc_04"]/div[1]/div[1]/div[2]/div[1]/div[1]/span/div[1]/div[1]/div[1]/div[1]/text()')[0].replace('发布日期：', '').replace(' ', '').replace('年', '-').replace('月', '-').replace('日','')
                        month1_1 = sub_xpath.xpath('//*[@id="tbc_04"]/div[1]/div[1]/div[2]/div[1]/div[1]/span/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/text()')
                        if month1_0 != '' and month1_1:
                            into(str(month1_0), str(month1_1[0]), rate, sub_name, str(type_value[3]), '成都中药材指数网',sub_url1, execution_time)
            except Exception as e:
                print(e)
                logg(log= str(e)+'获取数据异常')
                pass
            else:
                break

def typeclass(type_listname,type_listhref,rate,execution_time):
    print(type_listname)
    print(type_listhref)
    #//*[@id="tbc_01"]/div[1]/div[2]/div[2]/div[1]/div[1]/table/tbody/tr[2]/td[1]
    for i in range(len(type_listhref)):
        # into(rq,sj,Rate,mz,Value_type,Data_source,Web,execution_time)
        type_url = url+type_listhref[i]
        type_data = requests.get(type_url)
        type_xpath = etree.HTML(type_data.text)
        name = type_listname[i]
        if rate == '2':
            week_time1 = type_xpath.xpath('//*[@id="tbc_01"]/div[1]/div[2]/div[2]/div[1]/div[1]/table/tr[2]/td[1]/text()')[0]
            week_data1 = type_xpath.xpath('//*[@id="tbc_01"]/div[1]/div[2]/div[2]/div[1]/div[1]/table/tr[2]/td[2]/text()')[0]
            week_time2 = type_xpath.xpath('//*[@id="tbc_02"]/div[1]/div[2]/div[2]/div[1]/div[1]/table/tr[2]/td[1]/text()')[0]
            week_data2 = type_xpath.xpath('//*[@id="tbc_02"]/div[1]/div[2]/div[2]/div[1]/div[1]/table/tr[2]/td[2]/text()')[0]
            into(week_time1,week_data1,rate,name,type_value[0],'成都中药材指数网',type_url,execution_time)
            into(week_time2, week_data2,rate,name, type_value[1], '成都中药材指数网', type_url, execution_time)
        elif rate == '5':
            month_time1 = type_xpath.xpath('//*[@id="tbc_03"]/div[1]/div[2]/div[2]/div[1]/div[1]/table/tr[2]/td[1]/text()')[0]
            month_data1 = type_xpath.xpath('//*[@id="tbc_03"]/div[1]/div[2]/div[2]/div[1]/div[1]/table/tr[2]/td[2]/text()')[0]
            month_time2 = type_xpath.xpath('//*[@id="tbc_04"]/div[1]/div[2]/div[2]/div[1]/div[1]/table/tr[2]/td[1]/text()')[0]
            month_data2 = type_xpath.xpath('//*[@id="tbc_04"]/div[1]/div[2]/div[2]/div[1]/div[1]/table/tr[2]/td[2]/text()')[0]
            into(month_time1, month_data1,rate, name, type_value[2], '成都中药材指数网', type_url, execution_time)
            into(month_time2, month_data2,rate, name, type_value[3], '成都中药材指数网', type_url, execution_time)

def main(rate,execution_time):
    index = requests.get(_url)
    html = etree.HTML(index.text)
    type_listname = html.xpath('//*[@id="menulist"]/div/div/div/a[1]/text()')  # 获取大类名
    type_listhref = html.xpath('//*[@id="menulist"]/div/div/div/a[1]/@href')  # 获取大类名
    # typeclass(type_listname,type_listhref,rate,execution_time)
    t = threading.Thread(target=typeclass, args=(type_listname,type_listhref,rate,execution_time,))  # 定义线程，传入参数i
    t.start()  # 让线程开始工作

    for i in range(len(type_listname)):
        ra = i + 1
        subclass_name = html.xpath('//*[@id="menulist"]/div/div['+str(ra)+']/dl/dd/a/text()')# 获取小类名
        subclass_url = html.xpath('//*[@id="menulist"]/div/div['+str(ra)+']/dl/dd/a/@href')# 获取小类URL
        subclass_data = zip(subclass_name, subclass_url)

        th1 = threading.Thread(target=subclass, args=(subclass_data,execution_time,rate,))  # 定义线程，传入参数i
        th1.start()  # 让线程开始工作

if __name__ == '__main__':
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if len(sys.argv) > 1:
        print(sys.argv[1])
        if str(sys.argv[1]) == '2':
            logg(log='周数据采集开始执行')
            main(sys.argv[1], time)
        elif str(sys.argv[1]) == '5':
            logg(log='月数据采集开始执行')
            main(sys.argv[1], time)
        else:
            logg(log='参数异常')
    else:
        logg(log=str(time)+'参数不存在')
