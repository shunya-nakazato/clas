#!/usr/bin/env python3
"""
threading.py
-----------------
使い方:
    python threading.py

モジュール：
    - F9P: QZSS L1, L2
"""

import queue
import sys
import serial
from pyubx2 import UBXReader, NMEA_PROTOCOL, UBX_PROTOCOL


def f9p_thread_loop(f9p_port: str, f9p_baud: int = 115200, p: queue.Queue = None):
    try:
        with serial.Serial(f9p_port, f9p_baud, timeout=1) as f9p_ser:
            ubr = UBXReader(f9p_ser, protfilter=NMEA_PROTOCOL | UBX_PROTOCOL)
            while True:
                raw, parsed = read_ubx(ubr)
                if raw and parsed is not None:
                    p.put(parsed)
    except (serial.SerialException, TimeoutError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


def read_ubx(ubr: UBXReader):
    raw, parsed = ubr.read()  # ブロッキング
    return raw, parsed
