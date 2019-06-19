"""
dict 客户端

功能：根据用户输入,发送请求,得到结果
结构：一级界面--> 注册 登录 退出
     二级界面--> 查单词 历史记录 注销
"""

from socket import *
from getpass import getpass    #运行使用终端
import sys

ADDR = ('0.0.0.0',8000)

s = socket()
s.connect(ADDR)

def do_login(s):
    while True:
        name = input("请输入登录用户名:")
        passwd = getpass("请输入密码")
        msg = "L %s %s"%(name,passwd)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data == 'OK':
            print("登陆成功")
            login(name)
        else:
            print(data)
        return

def do_regist(s):
    while True:
        name = input("请输入注册用户名:")
        passwd = getpass("请输入密码")
        passwd_ = getpass("请再次输入密码:")

        if (' ' in name) or (' ' in passwd):
            print("用户名和密码不能有空格")
            continue
        if passwd != passwd_:
            print("两次密码输入不一致")
            continue
        msg = "R %s %s"%(name,passwd)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data == 'OK':
            print("注册成功")
            login(name)
        else:
            print("注册失败")
        return

def do_select(name,s):
    while True:
        word = input("请输入要查询的单词:")
        if word == '##':
            break
        msg = "S %s %s"%(name,word)
        s.send(msg.encode())
        data = s.recv(2048).decode()
        print(data)

def do_hist(name,s):
    msg = "H %s"%name
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        while True:
            data = s.recv(1024).decode()
            if data == '##':
                break
            print(data)
    else:
        print("没有历史记录")

def login(name):
    while True:
        print("""
            =====Query=====
                1.查询单词
                2.历史记录
                3.注销
            ===============
        """)
        cmd = input("请输入选项:")
        if cmd == '1':
            do_select(name,s)
        elif cmd == '2':
            do_hist(name,s)
        elif cmd == '3':
            return

def main():
    while True:
        print("""
            ====Welcome====
                1.注册
                2.登录
                3.退出
            ===============
        """)
        cmd = input("请输入选项:")
        if cmd == '1':
            do_regist(s)
        elif cmd == '2':
            do_login(s)
        elif cmd == '3':
            s.send(b'E')
            sys.exit("谢谢使用")
        else:
            print("请输入正确选项")

if __name__ == '__main__':
    main()
