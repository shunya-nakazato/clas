from pyubx2 import POLL, SET, UBX_CONFIG_DATABASE, U1

# 設定データベースの追加
UBX_CONFIG_DATABASE["CFG_MSGOUT_UBX_RXM_QZSSL6_USB"] = (0x2091033D, U1)
UBX_CONFIG_DATABASE["CFG_MSGOUT_UBX_RXM_QZSSL6_UART1"] = (0x2091033B, U1)

LAYER = {
    "RAM": 0x01,
    "BBR": 0x03,
    "FLASH": 0x07,
}

CMD_LIST_COMMON = {
    "UBX_MON_VER": lambda: {
        "ubxClass": 0x0A,
        "ubxID": 0x04,
        "msgmode": POLL,
    },
}

CMD_LIST = {
    "D9C": {
        **CMD_LIST_COMMON,
        "GET_CFG_MSGOUT_UBX_RXM_QZSSL6_UART1": lambda: {
            "ubxClass": 0x06,
            "ubxID": 0x8b,
            "msgmode": POLL,
            "payload": b"\x00\x00\x00\x00\x3b\x03\x91\x20",
        },
        "GET_CFG_MSGOUT_UBX_RXM_QZSSL6_USB": lambda: {
            "ubxClass": 0x06,
            "ubxID": 0x8b,
            "msgmode": POLL,
            "payload": b"\x00\x00\x00\x00\x3d\x03\x91\x20",
        },
        "GET_CFG_QZSS_L6_FFFF": lambda: {
            "ubxClass": 0x06,
            "ubxID": 0x8b,
            "msgmode": POLL,
            "payload": b"\x00\x00\x00\x00\xFF\xFF\x37\x20",
        },
        "GET_CFG_USBOUTPROT_UBX": lambda: {
            "ubxClass": 0x06,
            "ubxID": 0x8b,
            "msgmode": POLL,
            "payload": b"\x00\x00\x00\x00\x01\x00\x78\x10",
        },
        # Set commands
        "SET_CFG_MSGOUT_UBX_RXM_QZSSL6_UART1": lambda layer="RAM": {
            "ubxClass": 0x06,
            "ubxID": 0x8a,
            "msgmode": SET,
            "payload": b"\x00" + bytes([LAYER[layer]]) + b"\x00\x00\x3b\x03\x91\x20\x01",  # enable
        },
        "SET_CFG_MSGOUT_UBX_RXM_QZSSL6_USB": lambda layer="RAM": {
            "ubxClass": 0x06,
            "ubxID": 0x8a,
            "msgmode": SET,
            "payload": b"\x00" + bytes([LAYER[layer]]) + b"\x00\x00\x3d\x03\x91\x20\x01",  # enable
        },
        "SET_CFG_QZSSL6_SVIDA_ID3": lambda layer="RAM": {
            "ubxClass": 0x06,
            "ubxID": 0x8a,
            "msgmode": SET,
            "payload": b"\x00" + bytes([LAYER[layer]]) + b"\x00\x00\x20\x00\x37\x20\x07",  # チャンネルAを3号機に固定
        },
    },
    "F9P": {
        **CMD_LIST_COMMON,
        "GET_CFG_USBINPROT_FFFF": lambda: {
            "ubxClass": 0x06,
            "ubxID": 0x8b,
            "msgmode": POLL,
            "payload": b"\x00\x00\x00\x00\xFF\xFF\x77\x10",
        },
        "GET_CFG_USBOUTPROT_FFFF": lambda: {
            "ubxClass": 0x06,
            "ubxID": 0x8b,
            "msgmode": POLL,
            "payload": b"\x00\x00\x00\x00\xFF\xFF\x78\x10",
        },
        "GET_CFG_SIGNAL_FFFF": lambda: {
            "ubxClass": 0x06,
            "ubxID": 0x8b,
            "msgmode": POLL,
            "payload": b"\x00\x00\x00\x00\xFF\xFF\x31\x10",
        },
        # Set commands
        # Disable other satellites
        "SET_CFG_SIGNAL_FFFF": lambda layer="RAM": {
            "ubxClass": 0x06,
            "ubxID": 0x8a,
            "msgmode": SET,
            "payload": b"\x01" + bytes([LAYER[layer]]) + b"\x01\x00"
            + b"\x1f\x00\x31\x10\x01"  # enable GPS
            + b"\x01\x00\x31\x10\x01"  # enable GPS L1C/A
            + b"\x03\x00\x31\x10\x01"  # enable GPS L2
            + b"\x24\x00\x31\x10\x01"  # enable QZSS
            + b"\x12\x00\x31\x10\x01"  # enable QZSS L1
            + b"\x15\x00\x31\x10\x01"  # enable QZSS L2
            + b"\x21\x00\x31\x10\x01"  # disable Galileo
            + b"\x07\x00\x31\x10\x01"  # disable Galileo E1
            + b"\x0a\x00\x31\x10\x01"  # disable Galileo E5
            + b"\x22\x00\x31\x10\x01"  # disable BeiDou
            + b"\x0d\x00\x31\x10\x01"  # disable BeiDou B1
            + b"\x0e\x00\x31\x10\x01"  # disable BeiDou B2
            + b"\x25\x00\x31\x10\x01"  # disable GLONASS
            + b"\x18\x00\x31\x10\x01"  # disable GLONASS L1
            + b"\x1a\x00\x31\x10\x01"  # disable GLONASS L2
        },
        "SET_TRANSACTION_APPLY": lambda layer="RAM": {
            "ubxClass": 0x06,
            "ubxID": 0x8a,
            "msgmode": SET,
            "payload": b"\x01" + bytes([LAYER[layer]]) + b"\x03\x00",
        },
    }
}
