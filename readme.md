#成都药材指数网获取价格指数
* 1.如何运行
    * python3 /home/maolz/cdyc/main.py 参数2,5 参数2为周，参数5为月
* 2.代码文件
    * 定时执行代码文件为/home/maolz/cdyc/main.py
    * 获取历史数据代码文件为/home/maolz/cdyc/lishishuju.py
    * log在/home/maolz/cdyc/logs/下,每日自动生成
* 3 mysql
    * mysql路径信息
        * 数据库目录/var/lib/mysql/
        * 配置文件/usr/share/mysql（mysql.server命令及配置文件）
    * 账户信息
        * 账号:root
        * 密码:maolz_2018
        * 端口:3306
        * 库名:cdyc
        * 表名:tb_data
* 4 计划任务
    * crontab 任务在root用户下
        * 0 9-18 1-5 * * /usr/local/python3/bin/python3.6 /home/maolz/cdyc/main.py 5
            * 月数据：暂定每月1日至5日，上午9点至18点，每小时采集一次
        * 0 9-18 * * 1 /usr/local/python3/bin/python3.6 /home/maolz/cdyc/main.py 2 
            * 周数据：暂定每周一上午9点至18点，每小时采集一次

* 5 历史数据
    * 历史数据执行执行 python3 /home/maolz/cdyc/lishishuju.py 即可

* 6 注
    * 2018-11-15 更新
        * 在爬去中会存在 白药子* 带 * 的字段在反馈中说查找不到白药子这个字段，现在修改为去除*号,在数据库中remarks这个字段是原有的名字。
    * 2018-11-15-1更新
        * 删除了备注remarks这个字段,直接删除*符号,写入name字段
    * 历史数据在压缩包中的cdyc_new_ok.sql，在服务器上的位置/home/maolz/cdyc/sqlbak/2018-11-16-15-55.sql