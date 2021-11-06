from __future__ import print_function

import json

from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template
from werkzeug.debug import DebuggedApplication

from geventwebsocket import WebSocketServer, WebSocketApplication, Resource

flask_app = Flask(__name__)
flask_app.debug = True


class ChatApplication(WebSocketApplication):
    def on_open(self):
        print("Some client connected!")

    def on_message(self, message):
        if message is None:
            return

        message = json.loads(message)

        if message['msg_type'] == 'message':
            self.broadcast(message)
        elif message['msg_type'] == 'update_clients':
            self.send_client_list(message)

    def send_client_list(self, message):

        # ここで使用している，ソケット情報に関するまとめ．
        
        # self.ws: サーバソケットに対応する WebSocketオブジェクト
        # self.ws.handler: self.ws に紐付いた WebSocketHandlerオブジェクト
        # self.ws.handler.active_client: 現在対応しているクライアントに対応する
        #   Clientオブジェクト
        # self.ws.handler.server: サーバソケットに対応する WebSocketServer オブジェクト
        # self.ws.handler.server.clients: サーバソケットに接続しているクライアントの
        #   Clientオブジェクトのディクショナリ． Clientのアドレス（address属性）が
        #   キーになっている
        
        # Clientオブジェクトは，デフォルトで addressとwsの2つの属性を持つ．
        # addressは接続元のアドレス（'127.0.0.1'などの文字列）と，ポート番号（int）の
        # タプル（タプルなのでディクショナリのキーとして使える）．
        # wsは対応するWebSocketオブジェクト．

        # 下の例では，Clientオブジェクトに nickname属性を追加してチャット上でのクライアント
        # のニックネームを管理している．
        current_client = self.ws.handler.active_client
        current_client.nickname = message['nickname']

        self.ws.send(json.dumps({
            'msg_type': 'update_clients',
            'clients': [
                getattr(client, 'nickname', 'anonymous')
                for client in self.ws.handler.server.clients.values()
            ]
        }))

    def broadcast(self, message):
        for client in self.ws.handler.server.clients.values():
            client.ws.send(json.dumps({
                'msg_type': 'message',
                'nickname': message['nickname'],
                'message': message['message']
            }))

    def on_close(self, reason):
        print("Connection closed!")


@flask_app.route('/')
def index():
    return render_template('index.html')

WebSocketServer(
    ('0.0.0.0', 8000),

    Resource([
        ('^/chat', ChatApplication),
        ('^/.*', DebuggedApplication(flask_app))
    ]),

    debug=False
).serve_forever()
