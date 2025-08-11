import argparse
import sys
import serial
import binascii
import textwrap
from pyubx2 import UBXReader, NMEA_PROTOCOL, UBX_PROTOCOL
from constants.MODULE_LIST import MODULE_LIST
from utils.utils import dump_bytes, output_dict


def main():
    ap = argparse.ArgumentParser(description="Run u-blox streaming")
    ap.add_argument(
        "--module",
        required=True,
        help="Module name",
        choices=["d9c", "f9p"],
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
                if raw is not None:
                    # ── 出力 ───────────────────────────────────────────────
                    print()
                    dump_bytes(raw)
                    print()
                    output_dict(parsed)
                    print()
            # while True:
            #     data = ser.read(2048)       # 128 byte ずつブロック読み
            #     if data:
            #         # 16進文字列へ変換し、見やすく16byte折り返し
            #         hexstr = binascii.hexlify(data).decode()
            #         print("\n".join(textwrap.wrap(hexstr, 32)))
    except (serial.SerialException, TimeoutError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
