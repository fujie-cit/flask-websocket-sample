# flask-websocket-sample

## サーバプログラム

```
$ cd server
$ python chat.py
```

flaskベースで[gevent-websocket](https://pypi.org/project/gevent-websocket/)を使ったWebSocketサーバの例です．

ウェブブラウザでアクセスしてチャットに接続することが可能です．

## クライアントプログラム

```
$ cd client
$ python run.py
```

サーバに接続してチャットを行うことができるPythonプログラムの例です．
[websocket-client](https://pypi.org/project/websocket-client/)を利用して実装されています．


