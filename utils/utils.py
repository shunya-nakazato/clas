
def as_str_array(field):
    """bytes → str, 末尾の NUL を除去"""
    if isinstance(field, (bytes, bytearray)):
        return [
            chunk.decode(errors="ignore")
            for chunk in field.split(b"\x00")
            if chunk  # 空バイト列は捨てる
        ]
    return str(field)


def as_str(field):
    """bytes/bytearray → str（末尾 NUL 除去）"""
    if isinstance(field, (bytes, bytearray)):
        return field.split(b"\x00", 1)[0].decode(errors="ignore")
    return str(field)


def output_array(msg):
    clean_array = as_str_array(msg.payload)
    for item in clean_array:
        print(item)


def output_dict(msg):
    clean_dict = {k: as_str(v) for k, v in vars(msg).items() if not k.startswith("_")}
    if "UBX" in msg.__class__.__name__:
        print(f"Message Class: 0x{msg.msg_cls.hex().upper()}")
        print(f"Message ID: 0x{msg.msg_id.hex().upper()}")
    elif "NMEA" in msg.__class__.__name__:
        print(f"Message Talker: {msg.talker}")
        print(f"Message ID: {msg.msgID}")
    for k, v in clean_dict.items():
        print(f"{k}: {v}")


def dump_bytes(data: bytes) -> None:
    """バイト列を '0xXX' 形式で整形して表示する"""
    formatted = ' '.join(f'0x{b:02X}' for b in data)
    print(f"({len(data)} byte): {formatted}")
