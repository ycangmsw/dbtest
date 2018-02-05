#!/usr/bin/env python
#-*-coding:utf-8 -*-

# 2017-12-12

import sys
from conn_sql import ConnetToMysql
from datetime import datetime
from socket import *

reload(sys)
sys.setdefaultencoding('utf8')

# 通讯部分
HOST = '192.168.3.4'
PORT = 2145
BUFSIZE = 4096
ADDR = (HOST,PORT)

# 发送一条记录
# 参数:元组 tupdata
def SendData(tupdata):
    strinfo = ToStr(tupdata)
    tcpClientSocket = socket(AF_INET,SOCK_STREAM)
    tcpClientSocket.connect(ADDR)
    tcpClientSocket.send(strinfo)
    while True:
        temp = tcpClientSocket.recv(BUFSIZE)
        if temp == "ok":
            break
        else:
            print "没有收到OK!"
    tcpClientSocket.close()

# 将元组转换成字符串，并添加隔离字符
# 参数：元组 tupdata
def ToStr(tupdata):
    strtemp = ''
    for item in tupdata:
       strtemp = strtemp + str(item) + '#'
    print "strtemp:",strtemp
    return strtemp

if __name__ == '__main__':
    # 查询参数
    str_sql_query = "select * from sansiapp_aftersales where as_date between %s and %s"
    
    #str_sql_query = "select * from sansiapp_aftersales"
    tup_arg = () #设置查询条件

    # 备份最后一条同步记录
    backtemp = None

    MYDB=ConnetToMysql()
    MYDB.conn_db()

    cur = MYDB.sql_query(str_sql_query,tup_arg)
    data=cur.fetchall()
    row_cunt = cur.rowcount
    print '行数：',row_cunt
    for it in range(0,row_cunt):
        print "正在发送数据：",it
        SendData(data[it])


    MYDB.sql_close(cur)
    MYDB.sql_finish()
                
    print u'结束'


