import socket
import os
import json
import math
from tokenize import Double

class Udp_socket_with_file():
    def __init__(self):
        # socket.socket関数を使用して、新しいソケットを作成します。
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

        # サーバが接続を待ち受けるUNIXドメインソケットのパスを指定します。
        self.server_address = '/tmp/udp_socket_file'

        try:
            # もし前回の実行でソケットファイルが残っていた場合、そのファイルを削除します。
            os.unlink(self.server_address)
        except FileNotFoundError:
            # ファイルが存在しない場合は何もしません。
            pass

        # ソケットが起動していることを表示します。
        print('starting up on {}'.format(self.server_address))

        # sockオブジェクトのbindメソッドを使って、ソケットを特定のアドレスに関連付けます。
        self.sock.bind(self.server_address)


class Rpc_process():
    def __init__(self, socket : socket, functions: dict[str, callable]):
        self.socket = socket.sock
        self.functions = functions
        self.accept_byte = 4096

    def recieve(self):
        try:
            # ソケットはデータの受信を永遠に待ち続けます。
            while True:
                print('\nwaiting to receive message')

                # ソケットからのデータを受信します。
                # 4096は一度に受信できる最大バイト数です。
                data, address = self.socket.recvfrom(self.accept_byte)

                # 受信したデータのバイト数と送信元のアドレスを表示します。
                print('received {} bytes from {}'.format(len(data), address))
                print(data)

                request_data = json.loads(data.decode())

                rpc_result = self.rpc(request_data)

                self.response(rpc_result, address)

        except KeyboardInterrupt:
            pass


    def rpc(self, data):
        func = self.functions.get(data.get("method"))
        result = func(*data.get("params"))
        print(result)

        return {
                "results": result,
                "result_type": type(result).__name__,
                "id": data.get("id", 0)
                }


    def response(self, rpc_result, client_address):
        # 受信したデータをそのまま送信元に送り返します。
        if rpc_result:
            data = json.dumps(rpc_result)
            sent = self.socket.sendto(data.encode("utf-8"), client_address)
            # 送信したバイト数と送信先のアドレスを表示します。
            print('sent {} bytes back to {}'.format(sent, client_address))

# rpc functions
def floor(x: Double):
    return round(x)

def nroot(n: int, x: int):
    return math.pow(x, 1/n)

def reverse(s: str):
    return s[::-1]

def valid_anagram(str1: str, str2: str):
    if len(str1) != len(str2):
        return False

    for i in range(len(str1)):
        if str1[i] in str2:
            continue
        else:
            return False

    return True

def sort(s: str):
    return ''.join(sorted(s))

# server 起動　
def main():
    rpc_func_dict = {
        "floor" : floor,
        "nroot" : nroot,
        "reverse" : reverse,
        "validAnagram" : valid_anagram,
        "sort" : sort
    }

    soc = Udp_socket_with_file()

    rpc = Rpc_process(soc, rpc_func_dict)

    rpc.recieve()

if __name__ == "__main__":
    main()
