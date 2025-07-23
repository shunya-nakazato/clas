#!/usr/bin/env python3
"""
command.py
-----------------
u-blox D9C 系 GNSS モジュールのファームウェア (SW) / ハードウェア (HW) 版
および拡張バージョン情報を取得して表示するスクリプト。

使い方:
    python d9c_fw_version.py --port /dev/tty.usbmodem142401 --baud 115200
"""
import argparse
import sys
import serial
from pyubx2 import UBXMessage, UBXReader, POLL

UBX_CLASS_MON = 0x0A
UBX_ID_VER = 0x04


def poll_mon_ver(ser: serial.Serial, timeout=5.0):
    """
    MON-VER をポーリングし、応答メッセージ (UBX-MON-VER) を返す。
    """
    # --- リクエスト送信 ----------------------------------------------------
    req = UBXMessage(UBX_CLASS_MON, UBX_ID_VER, POLL)
    ser.write(req.serialize())

    # --- 応答受信 ----------------------------------------------------------
    ubr = UBXReader(ser, protfilter=2)  # UBX のみ受信
    ser.flush()
    for raw, parsed in ubr:
        if parsed.identity == "MON-VER":
            return parsed
        # 応答がなければ timeout
        if ser.timeout and ser.in_waiting == 0:
            raise TimeoutError("No MON-VER response within timeout")


def as_str(field):
    """bytes → str, 末尾の NUL を除去"""
    if isinstance(field, (bytes, bytearray)):
        return field.split(b"\x00", 1)[0].decode(errors="ignore")
    return str(field)


def main():
    ap = argparse.ArgumentParser(description="Read u-blox D9C firmware version")
    ap.add_argument(
        "--port",
        "-p",
        required=True,
        help="Serial port (e.g. /dev/tty.usbmodem142401 or COM3)",
    )
    ap.add_argument(
        "--baud", "-b", type=int, default=115200, help="Baud rate (default 115200)"
    )
    args = ap.parse_args()

    try:
        with serial.Serial(args.port, args.baud, timeout=1) as ser:
            ver = poll_mon_ver(ser)
    except (serial.SerialException, TimeoutError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    # ── 出力 ───────────────────────────────────────────────
    print("=== u-blox D9C Firmware Info ===")
    print("SW Version :", as_str(getattr(ver, "swVersion", b"")))
    print("HW Version :", as_str(getattr(ver, "hwVersion", b"")))

    # extension_01 … extension_20 などを動的に列挙
    for idx in range(1, 31):  # 30 本まで仕様上存在し得る
        name = f"extension_{idx:02d}"
        if hasattr(ver, name):
            val = as_str(getattr(ver, name))
            if val:  # 空ならスキップ
                print("EXT        :", val)


from pyubx2.ubxtypes_core import UBX_MSGIDS

if __name__ == "__main__":
    print(('MON', 'VER') in UBX_MSGIDS)   # True になるのが正常
    main()
