from pyubx2 import SET_LAYER_RAM, TXN_NONE, POLL, SET, UBX_CONFIG_DATABASE, U1

# 設定データベースの設定
UBX_CONFIG_DATABASE["CFG_MSGOUT_UBX_RXM_QZSSL6_USB"] = (0x2091033D, U1)
UBX_CONFIG_DATABASE["CFG_MSGOUT_UBX_RXM_QZSSL6_UART1"] = (0x2091033B, U1)

CMD_LIST = {
    "UBX-MON-VER": {
        "ubxClass": 0x0A,
        "ubxID": 0x04,
        "msgmode": POLL,
    },
    "GET-CFG-MSGOUT-UBX_RXM_QZSSL6_UART1": {
        "ubxClass": 0x06,
        "ubxID": 0x8b,
        "msgmode": POLL,
        "payload": b"\x00\x00\x00\x00\x3b\x03\x91\x20",
    },
    "GET-CFG-MSGOUT-UBX_RXM_QZSSL6_USB": {
        "ubxClass": 0x06,
        "ubxID": 0x8b,
        "msgmode": POLL,
        "payload": b"\x00\x00\x00\x00\x3d\x03\x91\x20",
    },
    "GET-CFG-QZSS-L6_FFFF": {
        "ubxClass": 0x06,
        "ubxID": 0x8b,
        "msgmode": POLL,
        "payload": b"\x00\x00\x00\x00\xFF\xFF\x37\x20",
    },
    "GET-CFG-USBOUTPROT-UBX": {
        "ubxClass": 0x06,
        "ubxID": 0x8b,
        "msgmode": POLL,
        "payload": b"\x00\x00\x00\x00\x01\x00\x78\x10",
    },
    # Set commands
    "SET-CFG-MSGOUT-UBX_RXM_QZSSL6_UART1": {
        "ubxClass": 0x06,
        "ubxID": 0x8a,
        "msgmode": SET,
        "payload": b"\x00\x01\x00\x00\x3b\x03\x91\x20\x00",
    },
    "SET-CFG-MSGOUT-UBX_RXM_QZSSL6_USB": {
        "ubxClass": 0x06,
        "ubxID": 0x8a,
        "msgmode": SET,
        "payload": b"\x00\x01\x00\x00\x3d\x03\x91\x20\x01",
    },
}
