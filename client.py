import socket
import os
import json

# UNIXドメインソケットとデータグラム（非接続）ソケットを作成します
sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

# サーバのアドレスを定義します。
# サーバはこのアドレスでメッセージを待ち受けます
server_address = '/tmp/udp_socket_file'

# このクライアントのアドレスを定義します。
# サーバはこのアドレスにメッセージを返します
address = '/tmp/udp_client_socket_file'

# サーバに送信するメッセージを定義します
try:
    # もし前回の実行でソケットファイルが残っていた場合、そのファイルを削除します。
    os.unlink(address)
except FileNotFoundError:
    # ファイルが存在しない場合は何もしません。
    pass

# このクライアントのアドレスをソケットに紐付けます。
# これはUNIXドメインソケットの場合に限ります。
# このアドレスは、サーバによって送信元アドレスとして受け取られます。
sock.bind(address)

call_floor = {
   "method": "floor", 
   "params": [42.999], 
   "param_types": ["int", "int"],
   "id": 1
}

call_nroot = {
   "method": "nroot", 
   "params": [3, 99], 
   "param_types": ["int", "int"],
   "id": 2
}

call_reverse = {
   "method": "reverse", 
   "params": ["abcdefg"], 
   "param_types": ["str"],
   "id": 3
}

call_validAnagram = {
   "method": "validAnagram", 
   "params": ["abcdefg", "gfeicba"], 
   "param_types": ["str", "str"],
   "id": 4
}

call_sort = {
   "method": "sort", 
   "params": ["fldjsaofgjnewoghnoierwhj"], 
   "param_types": ["str"],
   "id": 5
}

calls_test = [call_floor, call_nroot, call_reverse, call_validAnagram, call_sort]

try:
    # サーバにメッセージを送信します
    for c in calls_test:
        byte_message = json.dumps(c).encode("utf-8")

        print('sending {!r}'.format(byte_message))

        sent = sock.sendto(byte_message, server_address)

        # サーバからの応答を待ち受けます
        print('waiting to receive')
        # 最大4096バイトのデータを受け取ります
        data, server = sock.recvfrom(4096)

        # サーバから受け取ったメッセージを表示します
        print('received {!r}'.format(data))

except KeyboardInterrupt:
    pass

finally:
    # 最後にソケットを閉じてリソースを解放します
    print('closing socket')
    sock.close()