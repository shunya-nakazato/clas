from pyubx2 import SET_LAYER_RAM, TXN_NONE, POLL, SET, UBX_CONFIG_DATABASE, U1

# 設定データベースの設定
UBX_CONFIG_DATABASE["CFG_MSGOUT_UBX_RXM_QZSSL6_USB"] = (0x2091033D, U1)

CMD_LIST = {
    "UBX-MON-VER": {
        "ubxClass": 0x0A,
        "ubxID": 0x04,
        "msgmode": POLL,
    },
    "UBX-CFG-VALGET": {
        "ubxClass": 0x06,
        "ubxID": 0x8b,
        "msgmode": POLL,
        "payload": b"\x00\x00\x00\x00\x3d\x03\x91\x20",
    },
    "CFG-MSGOUT-UBX_RXM_QZSSL6_USB": {
        "ubxClass": 0x06,
        "ubxID": 0x8a,
        "msgmode": SET,
        "payload": b"\x00\x01\x00\x00\x3d\x03\x91\x20\x01",
    },
}