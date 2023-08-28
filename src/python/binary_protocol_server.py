#!/usr/bin/env python3

import socket
import struct

# このmsgがbytes型
def send_msg(sock, msg):
    total_sent_byte_length = 0
    total_message_byte_length = len(msg)
    while total_sent_byte_length < total_message_byte_length:
        # pythonのbytes型はgoのbyte sliceみたいな感じ
        sent_length = sock.send(msg[total_sent_byte_length:])
        if sent_length == 0:
            raise RuntimeError("socket connection broken")
        total_sent_byte_length += sent_length

def recv_msg(sock, total_msg_byte_size):
    total_recv_byte_size = 0
    while total_recv_byte_size < total_msg_byte_size:
        received_chunk = sock.recv(total_msg_byte_size - total_recv_byte_size)
        if len(received_chunk) == 0:
            raise RuntimeError("socket connection broken")
        yield received_chunk
        total_recv_byte_size += len(received_chunk)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server_socket.bind(("127.0.0.1", 54321))
    server_socket.listen()
    print("starting server...")
    client_socket, (client_address, client_port) = server_socket.accept()
    print(f"accepted from {client_address}:{client_port}")
    received_msg = b"".join(recv_msg(client_socket, total_msg_byte_size=8))
    print(f"received: {received_msg}")

    # バイト列を2つの32ビットの整数として解釈する
    # 次の部分で、受信したネットワークバイトオーダーのバイト列をホストバイトオーダーのバイト列に変換している
    # バイトオーダーの変換は、Pythonではstructモジュールを使って実現できます。
    # ネットワークバイトオーダーをホストバイトオーダーに変換するにはunpack()関数を使います。
    # 引数の'!ii'という文字列は、受信したバイト列を2つの4バイト整数として解釈する、という意味です
    (operand1, operand2) = struct.unpack("!ii", received_msg)
    print(f"operand1:{operand1}, operand2:{operand2}")
    result = operand1 + operand2

    print(f"result: {result}")
    # ホストバイトオーダーをネットワークバイトオーダーに変換しているのが次の部分です。
    # ホストバイトオーダーのバイト列からネットワークバイトオーダーのバイト列への変換にはpack()関数を使います。
    # ここでは計算した値を一つの64ビット(8バイト)の整数として解釈できるように変換しています。
    result_msg = struct.pack("!q", result)
    send_msg(client_socket, result_msg)
    print(f"sent: {result_msg}")

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()