#!/usr/bin/python3
import time
import os

from threading import Thread
from multiprocessing import Process

def fibonacci(n: int):
    a = 0
    b = 1
    for _ in range(n):
        a, b = b, a + b
    return a

def process():
    for _ in range(10):
        fibonacci(10000)

def sequential() -> float:
    start = time.time()
    for _ in range(10):
        process()
    end = time.time()
    return end - start

def threading() -> float:
    start = time.time()
    threads = []
    for _ in range(10):
        t = Thread(target=process)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    end = time.time()
    return end - start

def processing() -> float:
    start = time.time()
    processes = []
    for _ in range(10):
        p = Process(target=process)
        processes.append(p)
        p.start()
    for tp in processes:
        p.join()
    end = time.time()
    return end - start

if __name__ == "__main__":
    seq = sequential()
    thr = threading()
    pro = processing()
    with open("artifacts/1-RESULT.txt", "w") as f:
        f.write(str(seq) + os.linesep)
        f.write(str(thr) + os.linesep)
        f.write(str(pro) + os.linesep)
