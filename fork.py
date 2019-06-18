"""
基于fork的进程创建演示
"""

import os

print("old")
pid = os.fork()
print(pid)

if pid < 0:
    print("Create process failed")
elif pid == 0:
    print("New process")
else:
    print("Old process")

print("Fork test end")