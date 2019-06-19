"""
dict database
提供服务端的所有数据库操作
"""

import pymysql
import hashlib
import re

SALT = "#&AID_"

class Database:
    def __init__(self,host = 'localhost',
                      port = 3306,
                      user = 'root',
                      passwd = '123456',
                      database = 'dict',
                      charset = 'utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.connect_db()

    def connect_db(self):
        self.db = pymysql.connect(host = self.host,
                                  port = self.port,
                                  user = self.user,
                                  passwd = self.passwd,
                                  database = self.database,
                                  charset = self.charset,
                                 )

    def create_cursor(self):
        self.cur = self.db.cursor()

    def close(self):
        self.db.close()

    def register(self,name,passwd):
        sql = "select * from user where name = '%s'"%name
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return False
        else:
            hash = hashlib.md5((name+SALT).encode())
            hash.update(passwd.encode())
            passwd = hash.hexdigest()
            sql = "insert into user (name,passwd) values (%s,%s)"
            try:
                self.cur.execute(sql,[name,passwd])
                self.db.commit()
                return True
            except Exception:
                self.db.rollback()
                return False

    def login(self,name,passwd):
        hash = hashlib.md5((name+SALT).encode())
        hash.update(passwd.encode())
        passwd = hash.hexdigest()
        sql = "select * from user where name = '%s' and passwd = '%s'"%(name,passwd)
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return True
        else:
            return False

    def select(self,word):
        sql = "select mean from words where word = '%s'"%(word)
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return r[0]

    def insert_history(self,name,word):
        sql = "insert into history (name,word) values (%s,%s)"
        try:
            self.cur.execute(sql,[name,word])
            self.db.commit()
        except Exception:
            self.db.rollback()

    def history(self,name):
        sql = "select name,word,time from history where name = '%s' order by time desc limit 10"%name
        self.cur.execute(sql)
        return self.cur.fetchall()