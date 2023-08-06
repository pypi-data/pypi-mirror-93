![Upload Python Package](https://github.com/zunda-pixel/sRemo/workflows/Upload%20Python%20Package/badge.svg)

# sRemoAPI
sRemoAPI is a Python client for the [sCloud API](https://sremosup.socinno.com/page-2872/).

## sCloud API
[sCloud API](https://sremosup.socinno.com/page-2872/)とはSocinnoが販売しているスマートリモコン「sRemoシリーズ」のAPIです。
httpのGET/POSTで家電の操作が可能です。

## Example Code
このsRemoAPIのExample Code(.ipynb)をGoogle Colabで確認できるようにしています。

## Install
PyPIにアップロードしたので、pipでインストール可能です。
[PyPI sRemoAPI](https://pypi.org/project/sRemoAPI/)
```shell
pip install sRemoAPI
```

## How to use
必要なものはAPIのアクセストークンとsRemo本体の識別子です。

### Import
最初にAPIのアクセストークンと本体の識別子を入力する必要があります。

```python
from sRemo import sRemoAPI

access_token = ""
device_identify = ""

api = sRemoAPI(access_token, device_identify)
```

### set_adjustment()
センサーのずれを調整します。

### get_sensor_data()
センサーの情報(温度、湿度、照度)を取得可能です。

### get_time()
時間が取得可能です。
これは必要あるのかわからないですが、sCloud APIにあるので実装しておきました。

### get_limit()
sCloud APIは5分で10回までアクセス可能で、このメソッドでは今何回アクセスしたかが確認可能です。
しかしこのアクセス数を確認するためにアクセスを1つ無駄にしているので、使わなくても問題ないと思います。


### send_signal_141()
sRemoのアプリで141個まで登録可能なカスタムボタンを実行できるものです。
ボタンの番号を引数にとります。

### send_signal()
sRemoに登録した家電を操作可能です。
アプリで登録した家電番号、家電のタイプ、信号が必要です。
家電のタイプはget_appliances_type()で取得可能です。文字列で渡してください。
信号はsCloud APIの解説から確認可能です。
sCloud APIの解説ではエアコンを別で説明していますが、どちらもsend_signal()で対応可能です。

