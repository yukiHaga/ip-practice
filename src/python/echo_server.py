#!/usr/bin/env python3

# script that implements an echo server using sockets

import socket

def send_msg(sock, msg):
    total_sent_byte_length = 0

    total_msg_byte_length = len(msg)

    while total_sent_byte_length < total_msg_byte_length:
        sent_byte_length = sock.send(msg[total_sent_byte_length:])
        if sent_byte_length == 0:
            raise RuntimeError("socket connection broken")

        total_sent_byte_length += sent_byte_length


def recv_msg(sock, chunk_length = 1024):
    while True:
        # 実際、1回で全てのバイト列をソケットに書き込める保証はない。
        # そのため、このsend_msg()関数では、全てのバイト列が書き込まれるまで繰り返し処理を行います。
        # 指定したバイト数(chunk_length)だけデータを受信し、そのデータをバイナリ形式で返します。
        # つまり、一度にすべてのデータを受信するわけではありません。
        received_chunk = sock.recv(chunk_length)

        if len(received_chunk) == 0:
            break

        # 受信したデータをジェネレータが返す値として登録する
        yield received_chunk

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # the solution to avoid "Address already in use" error.
    # このメソッドは、ソケットの挙動を変更するオプションを指定するためにあります。
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    # specify the IP address and port number to listen for connections from clients.
    # これはクライアントからの接続を待ち受けるIPアドレスとポートを指定するメソッドです。
    # ホストのIPアドレスは、ひとつとは限りません。ネットワークインターフェイスが複数あれば、
    # IPアドレスも複数あるかもしれないからです。あるいは、ひとつのネットワークインターフェイスに、
    # 複数のIPアドレスが付与されることもあります。そのため、どのIPアドレスを使ってクライアントからの接続を待ち受けるか、
    # bind()メソッドを使って指定します。もし、すべてのIPアドレスで接続を待ち受けるときは
    # IPアドレスとして''(空文字)を指定します。
    server_socket.bind(("127.0.0.1", 54321))

    print("starting server.....")

    # handle the connection.
    # ソケットのインスタンスに対してaccept()メソッドを呼び出しています。
    # このメソッドは、実際にクライアントから接続があったときに、それを処理するためのものです。
    # accept()メソッドからは、クライアントを表したソケットのインスタンスと、
    # 接続してきたクライアントの情報が得られます。接続してきたクライアントの情報というのは、
    # 具体的には送信元のIPアドレスとポート番号です。IPアドレスはループバックアドレスになっているはずですが、
    # ポート番号はエフェメラルポートなので毎回異なります。
    client_socket, (client_address, client_port) = server_socket.accept()

    # display information about connected client.
    print(f"accepted from {client_address}:{client_port}")

    # Read byte sequence from the socket.
    for received_msg in recv_msg(client_socket):
        # write the read content back to the socket as it is(echo back).
        send_msg(client_socket, received_msg)

        print(f"echo: {received_msg}")

    # close the socket after it is no longer needed.
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()