import time
import math
import os
import multiprocessing

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def integrate_original(f, a, b, *, n_jobs=1, n_iter=1000):
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def process_part(start, end, step, f, a):
    print(f"Task from {start} to {end} started at {time.time()}")
    acc = 0
    for i in range(start, end):
        acc += f(a + i * step) * step
    return acc


def integrate(f, a, b, pool_class, *, n_jobs=1, n_iter=1000):
    step = (b - a) / n_iter
    with pool_class() as executor:
        iter_step = (n_iter + n_jobs - 1) // n_jobs
        futures = [executor.submit(process_part, start, min(
            n_iter, start + iter_step), step, f, a) for start in range(0, n_iter, iter_step)]
        acc = 0
        for future in futures:
            acc += future.result()
        return acc


def measure(pool_class, n_jobs):
    f = math.cos
    a = 0
    b = math.pi / 2
    n_iter = 1000
    start = time.time()
    result = integrate(f, a, b, pool_class, n_jobs=n_jobs, n_iter=n_iter)
    end = time.time()
    assert math.isclose(result, integrate_original(
        f, a, b, n_jobs=n_jobs, n_iter=n_iter))
    return end - start


if __name__ == "__main__":
    thread_times = []
    process_times = []
    print("Threads")
    for i in range(1, 2 * multiprocessing.cpu_count() + 1):
        t = measure(ThreadPoolExecutor, i)
        print(f"Time: {t} seconds")
        print()
        thread_times.append(t)

    print("Processes")
    for i in range(1, 2 * multiprocessing.cpu_count() + 1):
        t = measure(ProcessPoolExecutor, i)
        print(f"Time: {t} seconds")
        print()
        process_times.append(t)

    print("Compare")
    for i in range(len(thread_times)):
        thread_time = thread_times[i]
        process_time = process_times[i]
        print(f"{i + 1} threads. diff: {process_time - thread_time} process: {process_time} thread: {thread_time}")
