from chat_client import ChatClient

client = ChatClient()
client.start()

# コンソールから1行分の文字列を読み込み，
#   /nickname で始まる場合はニックネーム更新（＋ユーザ名取得）
#   その他であれば，メッセージとして送信
while True:
    line = input()

    if line.startswith("/nickname"):
        _, nickname = line.split(' ', 1)
        client.update_clients(nickname)
    else:
        client.send_message(line)
