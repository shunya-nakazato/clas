# u-blox CLAS モジュール用 Python スクリプト

このリポジトリは、u-blox社製 **D9C** および **F9P** モジュールを対象に、  
PythonからCLAS（センチメータ級測位補強サービス）関連コマンドを送受信するためのスクリプトを提供します。

---

## 対象モジュールとインタフェース仕様書

本スクリプトは以下のモジュールおよび公式インタフェース仕様書を前提としています。

- **ZED-F9P**
  - [u-blox ZED-F9P Interface Description (UBX-18010854)](https://www.geosense.co.jp/download/product/f9px1/u-blox_ZED-F9P_InterfaceDescription_(UBX-18010854).pdf)

- **D9C**
  - [u-blox D9C Interface Description (UBX-21031777)](https://content.u-blox.com/sites/default/files/u-blox-D9-QZS-1.01_InterfaceDescription_UBX-21031777.pdf)

---

## 使用ライブラリ

本スクリプトは、u-blox UBXプロトコルをPythonから扱うためのライブラリ **[pyubx2](https://github.com/semuconsulting/pyubx2)** を利用しています。

- UBXメッセージの生成、解析に `pyubx2` を使用
- 新規コマンドの登録時は `pyubx2/src/pyubx2/ubxtypes_configdb.py` 内の **`UBX_CONFIG_DATABASE`** に未定義のコマンドを追加してください

---

## コマンド定義

コマンドは `CMD_LIST.py` にて定義されています。  
**ペイロードのバイト列は必ずリトルエンディアンで記述**してください。

```python
CMD_LIST = {
    "EXAMPLE_CMD": {
        "ubxClass": 0x06,
        "ubxID": 0x8A,
        "payload": b"\x01\x00"  # リトルエンディアン
    },
}
```

---

## 主な機能

- UBXコマンドの送信（POLL, SET, GETなど）
- UBXレスポンスの受信・解析
- CLAS関連設定の読み取り・変更

---

## 動作環境

- Python 3.8+
- `pyubx2` ライブラリ

インストール例:
```bash
pip install pyubx2
```

---

## 使用例

```bash
python ubx_cmd.py --command UBX_MON_VER
```

---

## 注意事項

- 本スクリプトは公式SDKではなく、動作保証はありません。使用は自己責任でお願いします。
- 対象モジュールやファームウェアバージョンにより、利用できないコマンドがあります。
- UBXペイロードのエンディアン間違いに注意してください。
