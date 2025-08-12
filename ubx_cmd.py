#!/usr/bin/env python3
"""
ubx_cmd.py
-----------------
使い方:
    python ubx_cmd.py --module D9C --command UBX_MON_VER
    python ubx_cmd.py --module D9C --command SET_CFG_MSGOUT_UBX_RXM_QZSSL6_USB --layer RAM

モジュール：
    - D9C: QZSS L6
    - F9P: QZSS L1, L2
"""

from pyubx2 import UBXMessage, UBXReader, UBX_PROTOCOL
import argparse
import sys
import serial
from constants.MODULE_LIST import MODULE_LIST
from constants.CMD_LIST import CMD_LIST, LAYER
from utils.utils import dump_bytes, output_dict


def ubx_cmd(ser: serial.Serial, command: str, layer: str):
    # --- リクエスト送信 ----------------------------------------------------
    req = layer and UBXMessage(**CMD_LIST[command](layer=layer)) or UBXMessage(**CMD_LIST[command]())
    ser.write(req.serialize())

    # --- 応答受信 ----------------------------------------------------------
    ubr = UBXReader(ser, protfilter=UBX_PROTOCOL)  # UBX のみ受信
    ser.flush()
    for raw, parsed in ubr:
        return raw, parsed


def main():
    ap = argparse.ArgumentParser(description="Run u-blox command")
    ap.add_argument(
        "--module",
        required=True,
        help="Module name",
        choices=MODULE_LIST.keys(),
    )
    ap.add_argument(
        "--command",
        required=True,
        help="Command name",
        choices=CMD_LIST.keys(),
    )
    ap.add_argument(
        "--layer",
        required=False,
        help="Layer",
        choices=LAYER.keys(),
    )
    ap.add_argument(
        "--baud", type=int, default=115200, help="Baud rate (default 115200)"
    )
    args = ap.parse_args()

    try:
        with serial.Serial(MODULE_LIST[args.module]["PORT"], args.baud, timeout=1) as ser:
            raw, parsed = ubx_cmd(ser, args.command, args.layer)
    except (serial.SerialException, TimeoutError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    # ── 出力 ───────────────────────────────────────────────
    print()
    # dump_bytes(raw)
    print()
    output_dict(parsed)
    print()


if __name__ == "__main__":
    main()
