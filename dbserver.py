#!/usr/bin/env python
#-*-coding:utf-8 -*-
# 2017-12-14

import sys,os,time
from conn_sql import ConnetToMysql
from datetime import datetime
from socket import *

reload(sys)
sys.setdefaultencoding('utf8')

# 通讯部分
HOST = '192.168.2.2'
PORT = 2145
BUFSIZE = 4096
ADDR = (HOST,PORT)

# 数据库查询,通过 id 查询MySQL数据库，若查不到则插入一条数据记录
# 参数：以列表组织的一条记录
def QueryDB(lData):
    # 查询参数
    str_sql_query = "select * from sansiapp_aftersales where id=%s"
    strid = lData[0] # 取传入记录的id值
    tup_arg = (strid,) #设置查询条件

    MYDB=ConnetToMysql()
    MYDB.conn_db()

    try:
	cur = MYDB.sql_query(str_sql_query,tup_arg)
	data=cur.fetchall()
    except Exception,e:
        WriteError(e)
        sys.exit(1)
    if len(data) == 1:
        str_temp = "记录"+lData[0]+"存在\n"
        WriteInfo(str_temp)
    else:
        str_temp = "记录"+lData[0]+"不存在\n"
        WriteInfo(str_temp)
        try:
            MYDB.sql_insert(tuple(lData))
        except Exception,e:
            WriteError(e)
            MYDB.sql_close(cur)
            MYDB.sql_finish()
            sys.exit(1)

        str_temp = "增加记录"+" "+lData[0]+"\n"
        WriteInfo(str_temp)

    MYDB.sql_close(cur)
    MYDB.sql_finish()
    WriteInfo("数据库查询结束！\n")                   

# 将错误信息写入error文件
def WriteError(str_err_info):
    fp = open('error','a')
    str_temp = '['+time.ctime()+']'+' '+'错误记录：'+str_err_info+'\n'
    fp.write(str_temp)
    fp.close()

# 将信息写入info文件
def WriteInfo(str_info):
    fp = open('info','a')
    str_temp = '['+time.ctime()+']'+' '+str_info+'\n'
    fp.write(str_temp)
    fp.close()

def main():

    #记录错误的文件存在继续，若不存在就退出
    if not os.path.isfile('error'):
        print "error 文件不存在，即将退出！"
        sys.exit(0)

    # 接收数据列表
    listData = None

    tcpServerSocket = socket(AF_INET,SOCK_STREAM)
    tcpServerSocket.bind(ADDR)
    tcpServerSocket.listen(1)

    while True:
        listData = None
        WriteInfo("等待连接。。。")
        tcpClientSocket,addr = tcpServerSocket.accept()
        str_temp =  "连接来至："+str(addr)
        WriteInfo(str_temp)
        while True:
            try:
            	data = tcpClientSocket.recv(BUFSIZE)
            except socket.error,e:
                WriteError(e)
                sys.exit(1)
            if not len(data):
                break
            else:
                listData = data.split('#')
                listData = listData[:-1]
                QueryDB(listData)
                try:
                    tcpClientSocket.send("ok")
                except socket.error,e:
                    WriteError(e)
                    sys.exit(1)

        tcpClientSocket.close()

if __name__ == '__main__':
    main()

