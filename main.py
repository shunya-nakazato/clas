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
from utils.utils import output_msg

q = queue.Queue(maxsize=1000)


def main():
    ap = argparse.ArgumentParser(description="Run main")
    ap.add_argument(
        "--usb-transfer", 
        required=False,
        help="USB transfer is enabled",
        choices=["enable", "disable"],
    )
    args = ap.parse_args()

    # Transfer L6 messages from D9C to F9P by USB
    if args.usb_transfer == "enable":
        d9c_thread = threading.Thread(target=d9c_thread_loop, args=(MODULE_LIST["D9C"]["PORT"], MODULE_LIST["F9P"]["PORT"], 115200, 9600), daemon=True)
        d9c_thread.start()
    
    f9p_thread = threading.Thread(target=f9p_thread_loop, args=(MODULE_LIST["F9P"]["PORT"], 115200, q), daemon=True)
    f9p_thread.start()

    while True:
        parsed = q.get()
        if parsed is not None:
            output_msg(parsed)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
