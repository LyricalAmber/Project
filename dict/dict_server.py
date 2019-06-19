"""
dict 服务端

功能:业务逻辑处理
模型:多进程 tcp 并发
"""

from socket import *
from multiprocessing import Process
import signal
import sys
from operation_db import *
from time import sleep


HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)

db = Database()

def do_hist(c,data):
    name = data.split(' ')[1]
    r = db.history(name)
    if not r:
        c.send(b'Fail')
        return
    c.send(b'OK')
    for i in r:
        msg = "%s   %-16s   %s"%i
        sleep(0.01)
        c.send(msg.encode())
    sleep(0.01)
    c.send(b'##')

def do_select(c,data):
    tmp = data.split(' ')
    name = tmp[1]
    word = tmp[2]
    mean = db.select(word)
    if not mean:
        c.send("没有找到该单词".encode())
    else:
        msg = "%s : %s"%(word,mean)
        db.insert_history(name,word)
        c.send(msg.encode())

def do_login(c,data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    if db.login(name,passwd):
        c.send(b'OK')
    else:
        c.send('用户名不存在或用户名密码不正确'.encode())

def do_register(c,data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    if db.register(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'Fail')

def request(c):
    db.create_cursor()
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(),":",data)
        if not data or data[0] == "E":
            sys.exit()
        elif data[0] == "R":    #注册
            do_register(c,data)
        elif data[0] == "L":    #登录
            do_login(c,data)
        elif data[0] == "S":    #查询
            do_select(c,data)
        elif data[0] == "H":
            do_hist(c,data)

def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        try:
            c,addr = s.accept()
            print("connect from",addr)
        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit("服务端退出")
        except Exception as e:
            print(e)
            continue
        p = Process(target = request,args=(c,))
        p.daemon = True
        p.start()

if __name__ == '__main__':
    main()