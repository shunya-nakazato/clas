#!/usr/bin/env python3
"""
ubx_streaming.py
-----------------
使い方:
    python ubx_streaming.py --module D9C

モジュール：
    - D9C: QZSS L6
    - F9P: QZSS L1, L2
"""

import argparse
import sys
import serial
from pyubx2 import UBXReader, NMEA_PROTOCOL, UBX_PROTOCOL
from constants.MODULE_LIST import MODULE_LIST
from utils.utils import dump_bytes, output_msg


def main():
    ap = argparse.ArgumentParser(description="Run u-blox streaming")
    ap.add_argument(
        "--module",
        required=True,
        help="Module name",
        choices=MODULE_LIST.keys(),
    )
    ap.add_argument(
        "--baud", type=int, default=115200, help="Baud rate (default 115200)"
    )
    args = ap.parse_args()

    try:
        with serial.Serial(MODULE_LIST[args.module]["PORT"], args.baud, timeout=1) as ser:
            ubr = UBXReader(ser, protfilter=NMEA_PROTOCOL | UBX_PROTOCOL)
            while True:
                raw, parsed = ubr.read()  # ブロッキング
                if raw and parsed is not None:
                    # ── 出力 ───────────────────────────────────────────────
                    dump_bytes(raw)
                    output_msg(parsed)
    except (serial.SerialException, TimeoutError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
