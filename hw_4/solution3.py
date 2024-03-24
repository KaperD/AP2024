from multiprocessing import Queue, Pipe, Process
import fileinput
import time
import codecs


def A(queue, ab_conn):
    while element := queue.get():
        new_element = element.lower()
        print(f"A sending {new_element} to B at {time.time()}")
        ab_conn.send(new_element)
        time.sleep(5)
    ab_conn.send(None)


def B(ba_conn, bm_conn):
    while element := ba_conn.recv():
        new_element = codecs.encode(element, 'rot_13')
        print(f"B sending {new_element} to Main at {time.time()}")
        bm_conn.send(new_element)


if __name__ == "__main__":
    queue = Queue(10)
    ab_conn, ba_conn = Pipe()
    bm_conn, mb_conn = Pipe()
    a = Process(target=A, args=(queue, ab_conn))
    a.start()
    b = Process(target=B, args=(ba_conn, bm_conn))
    b.start()
    for line in fileinput.input():
        line = line.strip()
        print(f"Main sending {line} to A at {time.time()}")
        queue.put(line)
        print(mb_conn.recv())
    queue.put(None)
    b.join()
    a.join()
