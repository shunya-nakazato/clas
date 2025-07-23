#!/usr/bin/env python3
"""
command.py
-----------------
使い方:
    python command.py --port /dev/tty.usbmodem142401 --baud 115200

モジュール：
    - D9C: QZSS L6
    - F9P: QZSS L1, L2
"""
from pyubx2 import UBXMessage, UBXReader, POLL, UBX_PROTOCOL
import argparse
import sys
import serial
from MODULE_LIST import MODULE_LIST
from CMD_LIST import CMD_LIST


def get_command(ser: serial.Serial, command: str):
    # --- リクエスト送信 ----------------------------------------------------
    req = UBXMessage(CMD_LIST[command]["UBX_CLASS_MON"], CMD_LIST[command]["UBX_ID_VER"], POLL)
    ser.write(req.serialize())

    # --- 応答受信 ----------------------------------------------------------
    ubr = UBXReader(ser, protfilter=UBX_PROTOCOL)  # UBX のみ受信
    ser.flush()
    for raw, parsed in ubr:
        if parsed.identity == "MON-VER":
            return parsed
        # 応答がなければ timeout
        if ser.timeout and ser.in_waiting == 0:
            raise TimeoutError("No MON-VER response within timeout")


def send_command(ser: serial.Serial, command: str):
    req = UBXMessage(CMD_LIST[command]["UBX_CLASS_MON"], CMD_LIST[command]["UBX_ID_VER"], POLL)
    ser.write(req.serialize())


# def as_str(field):
#     """bytes → str, 末尾の NUL を除去"""
#     if isinstance(field, (bytes, bytearray)):
#         return [
#             chunk.decode(errors="ignore")
#             for chunk in field.split(b"\x00")
#             if chunk  # 空バイト列は捨てる
#         ]
#     return str(field)
def as_str(field):
    """bytes/bytearray → str（末尾 NUL 除去）"""
    if isinstance(field, (bytes, bytearray)):
        return field.split(b"\x00", 1)[0].decode(errors="ignore")
    return str(field)


def output_dict(msg):
    clean_dict = {k: as_str(v) for k, v in vars(msg).items() if not k.startswith("_")}
    for k, v in clean_dict.items():
        print(f"{k}: {v}")


def main():
    ap = argparse.ArgumentParser(description="Run u-blox command")
    ap.add_argument(
        "--module",
        required=True,
        help="Module name",
        choices=["d9c", "f9p"],
    )
    ap.add_argument(
        "--command",
        required=True,
        help="Command name",
        choices=["UBX-MON-VER"],
    )
    ap.add_argument(
        "--baud", type=int, default=115200, help="Baud rate (default 115200)"
    )
    args = ap.parse_args()

    try:
        with serial.Serial(MODULE_LIST[args.module]["PORT"], args.baud, timeout=1) as ser:
            res = get_command(ser, args.command)
    except (serial.SerialException, TimeoutError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    # ── 出力 ───────────────────────────────────────────────
    output_dict(res)
    # print("=== u-blox D9C Firmware Info ===")
    # print("SW Version :", as_str(getattr(ver, "swVersion", b"")))
    # print("HW Version :", as_str(getattr(ver, "hwVersion", b"")))

    # # extension_01 … extension_20 などを動的に列挙
    # for idx in range(1, 31):  # 30 本まで仕様上存在し得る
    #     name = f"extension_{idx:02d}"
    #     if hasattr(ver, name):
    #         val = as_str(getattr(ver, name))
    #         if val:  # 空ならスキップ
    #             print("EXT:", val)


if __name__ == "__main__":
    main()
