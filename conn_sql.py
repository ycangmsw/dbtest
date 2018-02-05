#!/usr/bin/env python
#-*- coding:utf-8 -*-

# 2017-8-21 
# 只修改sql_insert()方法,满足readexcel.py要求。
#
# 2017-11-27
# 修改查询通用方法和返回所有结果的方法

import mysql.connector

class ConnetToMysql:
    def __init__(self,host='localhost',port=3306,user='root',passwd='sansi1.3',db='djangosansidb'):
        self.host=host
        self.port=port
        self.user=user
        self.passwd=passwd
        self.db=db
        self.conn=None

        # sql命令字符串
        self.str_sql_insert="insert into sansiapp_aftersales (id,as_date,as_number,as_type,as_flagtype,as_name,as_client,as_clientname,as_clientphone,as_clientaddress,as_cranetype,as_metertype,as_cranemodel,as_metermodel,as_faultdescribe,as_faultanalyze,as_faultresult) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    def conn_db(self):
        try:
        #    print "conn_db"
            self.conn= mysql.connector.connect(\
                    host=self.host,\
                    port = self.port,\
                    user=self.user,\
                    passwd=self.passwd,\
                    db =self.db,\
                    charset='utf8'
                    )
        except Exception,e:
            print Exception,":",e
        return self.conn

    #删除符合查询条件的数据
    #cur.execute("delete from student where age='9'")
    def sql_delete(self,tup):
        delete=("deldete from tb_production where %s")
        cur=self.conn.cursor()
        try:
            cur.execute(delete,tup)
        except:
            print "delete except!"
            self.conn.rollback()
        self.conn.commit()
        return cur

    #修改查询条件的数据 cur.execute("update student set class='3 year 1 class' where name = 'Tom'")
    # 参数：元组 tup( 字符串1，字符串2)
    #       字符串1：被更改项,多余一个时用逗号分开
    #       字符串2：条件，多余一个时用逗号分开
    def sql_update(self,tup):
        update=("update tb_production set %s where %s")
        cur=self.conn.curson()
        try:
            cur.execute(update,tup)
        except:
            print "update except!"
            self.conn.rollback()
        self.conn.commit()
        return cur

    # 插入一条数据
    # 参数：元组  tup=(datetime.date(2017,1,18),'20170118001','liuqiang','20170118001.jpg')
    def sql_insert(self,tup):
        insert = (self.str_sql_insert)
        cur=self.conn.cursor()
        try:
            cur.execute(insert,tup)
        except Exception,e:
            print "insert except!"
            print Exception,':',e
            print '======================='
            self.conn.rollback()
        self.conn.commit()
        return cur

    # 条件查询 通用方法
    # 参数：
    #      str_sql_query : sql命令字符串，举例，
    #               str_sql_query = "select * from sansiapp_aftersales where as_date between %s and %s"
    #      tup_arg : 给查询条件赋值，元组，举例：
    #               tup_arg = ('2017-9-1','2017-9-30')
    def sql_query(self,str_sql_query,tup_arg=()):
        cur=self.conn.cursor()
        if not tup_arg:   # 若tup_arg=(),返回所有查询结果,此时要求：str_sql_query = "select * from sansiapp_aftersales"
            return self.sql_query_all()
        else:
            query=(str_sql_query)
            try:
                cur.execute(query,tup_arg)
            except Exception,e:
                print "Query except!"
                print Exception,':',e
                print '======================='
                self.conn.rollback()
            return cur


    # 查询 返回所有数据
    # 参数：无参数
    #
    def sql_query_all(self):
        cur=self.conn.cursor()
        query=("select * from sansiapp_aftersales")
        print "into sql_query_all..."
        try:
            cur.execute(query)
        except Exception,e:
            print "Query except!"
            print Exception,':',e
            print '======================='
            self.conn.rollback()
        return cur

#    # 查询
#    # 参数：字典  dic={'pro_date'='','pro_number':'','pro_name':''}
#    def sql_query(self,dic):
#        cur=None
#        # 1.生产任务单查询
#        # 根据日期查询
#        if dic.get('pro_date',None)<>None and dic.get('pro_number',None)==None and dic.get('pro_name',None)==None:
#            query=("select * from tb_production where pro_date=%(pro_date)s")
#            cur=self.conn.cursor()
#            try:
#                cur.execute(query,{'pro_date':dic['pro_date']})
#            except:
#                print "query except!"
#                self.conn.rollback()
#
#        # 根据生产单号查询，只要有单号就忽略其他条件
#        if dic.get('pro_number',None)<>None:
#            query=("select * from tb_production where pro_number=%(pro_number)s")
#            cur=self.conn.cursor()
#            try:
#                cur.execute(query,{'pro_number':dic['pro_number']})
#            except:
#                print "query except!"
#                self.conn.rollback()
#
#        # 根据申请人姓名查询
#        if dic.get('pro_date',None)==None and dic.get('pro_number',None)==None and dic.get('pro_name',None)<>None:
#            query=("select * from tb_production where pro_name=%(pro_name)s")
#            cur=self.conn.cursor()
#            try:
#                cur.execute(query,{'pro_name':dic['pro_name']})
#            except:
#                print "query except!"
#                self.conn.rollback()
#
#         # 根据日期和姓名查询
#        if dic.get('pro_date',None)<>None and dic.get('pro_number',None)==None and dic.get('pro_name',None)<>None:
#            query=("select * from tb_production where pro_name=%(pro_name)s or pro_date=%(pro_date)s")
#            cur=self.conn.cursor()
#            try:
#                cur.execute(query,{'pro_name':dic['pro_name'],'pro_date':dic['pro_date']})
#            except:
#                print "query except!"
#                self.conn.rollback()
#
#        # 2.用户查询
#        if dic.get('user_name',None)<>None and dic.get('user_passwd',None)<>None:
#            query=("select * from tb_user where user_name=%(user_name)s")
#            cur=self.conn.cursor()
#            try:
#                cur.execute(query,{'user_name':dic['user_name']})
#            except Exception,e:
#                print "query except"
#                print Exception,":",e
#                self.conn.rollback()
#        return cur

    def sql_close(self,cur):
        print "cur===>"
        cur.close()

    def sql_finish(self):
        #print "sql_finish!"
        #self.conn.commit() # 修改数据库时调用
        self.conn.close()
