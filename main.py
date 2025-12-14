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

import argparse
import os
import sys
import queue
import threading
from d9c.d9c_threading import d9c_thread_loop
from f9p.f9p_threading import f9p_thread_loop
from constants.MODULE_LIST import MODULE_LIST
from utils.utils import output_msg
from dotenv import load_dotenv
from mqtt.utils.logger import setup_logging
from mqtt_subscribe import mqtt_subscribe


# Common settings
load_dotenv(".env")
# Local settings (override if exists)
load_dotenv(".local.env", override=True)

# MQTT Configuration from environment variables
BROKER_HOST = os.getenv('MQTT_BROKER_HOST', 'localhost')
BROKER_PORT = int(os.getenv('MQTT_BROKER_PORT', '1883'))
TOPIC = os.getenv('MQTT_TOPIC', 'test/topic')
KEEPALIVE = int(os.getenv('MQTT_KEEPALIVE', '60'))

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
LOG_TO_FILE = os.getenv('LOG_TO_FILE', 'true').lower() == 'true'
LOG_TO_CONSOLE = os.getenv('LOG_TO_CONSOLE', 'true').lower() == 'true'
LOG_DIR = os.getenv('LOG_DIR', './log')

# Setup logger (only once!)
logger = setup_logging("subscriber", log_level=LOG_LEVEL, log_to_file=LOG_TO_FILE,
                       log_to_console=LOG_TO_CONSOLE, log_dir=LOG_DIR)

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

    mqtt_thread = threading.Thread(target=mqtt_subscribe, args=(logger, BROKER_HOST, BROKER_PORT, TOPIC, KEEPALIVE), daemon=True)
    mqtt_thread.start()

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
