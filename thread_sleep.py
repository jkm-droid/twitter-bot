import threading
import time


def print_hello():
    for i in range(4):
        time.sleep(10)
        print("Hello")


def print_hi():
    for i in range(4):
        time.sleep(5)
        print("Hi")

t1 = threading.Thread(target=print_hello)
t2 = threading.Thread(target=print_hi)
t1.start()
t2.start()
