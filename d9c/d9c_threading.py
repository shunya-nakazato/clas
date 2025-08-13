#!/usr/bin/env python3
"""
threading.py
-----------------
使い方:
    python threading.py

モジュール：
    - D9C: QZSS L6
"""

import sys
import serial
from pyubx2 import UBXReader, NMEA_PROTOCOL, UBX_PROTOCOL


def d9c_thread_loop(d9c_port: str, f9p_port: str, d9c_baud: int = 115200, f9p_baud: int = 115200):
    try:
        with serial.Serial(d9c_port, d9c_baud, timeout=1) as d9c_ser:
            with serial.Serial(f9p_port, f9p_baud, timeout=1) as f9p_ser:
                ubr = UBXReader(d9c_ser, protfilter=NMEA_PROTOCOL | UBX_PROTOCOL)
                while True:
                    raw, parsed = read_ubx(ubr)
                    if raw and parsed is not None:
                        write_ubx(f9p_ser, raw)
    except (serial.SerialException, TimeoutError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


def read_ubx(ubr: UBXReader):
    raw, parsed = ubr.read()  # ブロッキング
    return raw, parsed


def write_ubx(ser: serial.Serial, raw: bytes):
    ser.write(raw)
