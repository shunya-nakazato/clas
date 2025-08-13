#!/usr/bin/env python3
"""
main.py
-----------------
使い方:
    python main.py

モジュール：
    - D9C: QZSS L6
    - F9P: QZSS L1, L2
"""

import sys
import queue
import threading
from d9c.d9c_threading import d9c_thread_loop
from f9p.f9p_threading import f9p_thread_loop
from constants.MODULE_LIST import MODULE_LIST
from utils.utils import output_dict

q = queue.Queue(maxsize=1000)


def main():
    d9c_thread = threading.Thread(target=d9c_thread_loop, args=(MODULE_LIST["D9C"]["PORT"], MODULE_LIST["F9P"]["PORT"], 115200, 115200), daemon=True)
    f9p_thread = threading.Thread(target=f9p_thread_loop, args=(MODULE_LIST["F9P"]["PORT"], 115200, q), daemon=True)
    d9c_thread.start()
    f9p_thread.start()

    while True:
        parsed = q.get()
        if parsed is not None:
            print()
            output_dict(parsed)
            print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
