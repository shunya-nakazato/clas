import sys
import serial
from utils.utils import dump_bytes

PORT = "/dev/tty.usbmodem142401"
BAUD = 115200


def dump_bytes(data: bytes) -> None:
    """バイト列を '0xXX' 形式で整形して表示する"""
    formatted = ' '.join(f'0x{b:02X}' for b in data)
    print(f"({len(data)} byte): {formatted}")


def main():
    try:
        with serial.Serial(PORT, BAUD, timeout=1) as ser:
            while True:
                data = ser.read(2048)
                if data:
                    dump_bytes(data)
    except (serial.SerialException, TimeoutError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
