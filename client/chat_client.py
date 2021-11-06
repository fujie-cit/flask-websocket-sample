import websocket
import threading
import json

class ChatClient:
    """ウェブソケットでチャットアプリに接続してメッセージの送受信をするためのクラス
    """
    def __init__(self, url="ws://localhost:8000/chat", nickname=None):
        # ウェブソケットに接続する
        self._websocket_app = websocket.WebSocketApp(
            url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close)
        # アプリをバックグラウンドで動かすためのスレッド
        self._thread = threading.Thread(target=self._websocket_app.run_forever)
        # ニックネーム        
        self._nickname = nickname if nickname else "anonymous"

    def start(self):
        """スレッドを開始する
        """
        self._thread.start()

    def send_message(self, message):
        """メッセージを送る

        Args:
            message (str): 送るメッセージ
        """
        self._send(json.dumps(dict(
            msg_type="message",
            nickname=self._nickname,
            message=message
        )))

    def update_clients(self, nickname=None):
        """ニックネームの設定，およびユーザリスト取得のコマンドを送信する．
        ニックネームが与えられていない場合はanonymousにする．

        Args:
            nickname (str, optional): 設定するニックネーム. Defaults to None.
        """
        self._nickname = nickname if nickname else "anonymous"
        self._send(json.dumps(dict(
            msg_type="update_clients",
            nickname=self._nickname
        )))

    def _on_open(self, ws):
        """サーバに接続したときに呼び出されるコールバック関数．

        Args:
            ws (WebSocket): WebSocket
        """
        pass

    def _on_message(self, ws, message):
        """メッセージを受信したときに呼び出されるコールバック関数．

        Args:
            ws (WebSocket): WebSocket
            message (str): 受信したメッセージ（文字列）
        """
        msg = json.loads(message)
        if msg['msg_type'] == 'message':
            print("{}: {}".format(
                msg['nickname'], msg['message']
            ))
        elif msg['msg_type'] == 'update_clients':
            print("current clients:")
            for client_name in msg["clients"]:
                print("\t{}".format(client_name))

    def _on_error(self, ws):
        """エラーが起こったときに呼び出されるコールバック関数．

        Args:
            ws (WebSocket): WebSocket
        """

    def _on_close(self, ws):
        """接続が切断したときに呼び出されるコールバック関数．

        Args:
            ws (WebSocket): WebSocket
        """

    def _send(self, message):
        """サーバにメッセージを送信する

        Args:
            message (str): 送信するメッセージ（文字列）
        """
        self._websocket_app.send(message)
