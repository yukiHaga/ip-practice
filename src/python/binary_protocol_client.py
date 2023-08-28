#!/usr/bin/env python3

import socket
import struct

def send_msg(sock, msg):
    total_sent_byte_length = 0

    # get the length of a string
    total_msg_byte_length = len(msg)

    while total_sent_byte_length < total_msg_byte_length:
        # write a byte sequence to a socket and obtain the nubmer of bytes written.
        # an array that includes elements from index total_sent_byte_lenght to the end
        sent_byte_length = sock.send(msg[total_sent_byte_length:])

        if sent_byte_length == 0:
            raise RuntimeError("socket connection broken")

        total_sent_byte_length += sent_byte_length

def recv_msg(sock, total_msg_size):
    total_recv_size = 0

    while total_recv_size < total_msg_size:
        received_chunk = sock.recv(total_msg_size - total_recv_size)
        if len(received_chunk) == 0:
            raise RuntimeError("socket connection broken")
        yield received_chunk
        total_recv_size += len(received_chunk)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 54321))

    operand1, operand2 = 1000, 2000

    print(f"operand1: {operand1}, operand2: {operand2}")

    # ネットワークバイトオーダーのバイト列に変換する
    request_msg = struct.pack("!ii", operand1, operand2)

    # ソケットにバイト列を書き込む
    send_msg(client_socket, request_msg)
    print(f"sent: {request_msg}")

    # ソケットからバイト列を読み込む
    received_msg = b"".join(recv_msg(client_socket, 8))
    # 読み込んだバイト列を表示する
    print(f"received: {received_msg}")

    # 64ビットの整数として解釈する
    (added_value, ) = struct.unpack("!q", received_msg)

    print(f"result: {added_value}")
    client_socket.close()

if __name__ == "__main__":
    main()