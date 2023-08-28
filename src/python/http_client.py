#!/usr/bin/env python3
# if sheban exitsts, run script with python3

# http client script with socket

# the socket module is imported
# the socket module in Python provides the API for working with sockets
import socket

# function to write the specified byte sequence to the socket.
# Actually, it is not guaranteed that you can write the entire byte sequence to the socket in one go.
# Therefore, in this send_msg() function, it iteratively repeats the process until all the byte sequence is written.
# Inside the function, it repeatedly calls the send() method on the instance of the socket to write the byte sequence.
def send_msg(sock, msg):
    total_sent_byte_length = 0

    # get the length of a string
    total_msg_byte_length = len(msg)

    while total_sent_byte_length < total_msg_byte_length:
        # write a byte sequence to a socket and obtain the number of bytes written.
        # an array that includes elements from index total_sent_byte_length to the end
        sent_byte_length = sock.send(msg[total_sent_byte_length:])

        if sent_byte_length == 0:
            raise RuntimeError("socket connection broken")

        total_sent_byte_length += sent_byte_length

# generator function that reads byte sequence from a socket until the connection is closed.
# To read the response that should have been sent from the HTTP server, you can read it from the socket.
def recv_msg(sock, chunk_len=1024):
    while True:
        # read a specified number of bytes from a socket
        received_chunk = sock.recv(chunk_len)

        # When you are unable to read anything at all, it means that the connection has been closed.
        if len(received_chunk) == 0:
            break

        # return the received byte sequence
        yield received_chunk

def main():
    # prepare a socket for communication using IPv4/TCP.
    # An instance of a socket is created using the s
    # socket.AF_INET specifies the use of IPv4 as the network layer protocol.
    # socket.SOCK_STREAM specifies the use of TCP as the transport layer protocol.
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # The created instance of the socket is used to connect to the server
    # connect to the TCP/80 port of the loopback address.
    # to connect to the server, you call the connect() method on the instance of the socket.
    # this method takes the IP address and port number of the server as parameters.
    client_socket.connect(("127.0.0.1", 8000))

    request_text = "GET / HTTP/1.0\r\n\r\n"

    # to write data to a socket, you need to provide a byte array instead of a string.
    # encode a string into a byte sequence using ASCII encoding.
    # ASCII エンコーディングは、英数字や一部の記号をエンコードするための文字エンコーディング方式です。文字列をバイト列に変換することで、文字列をバイト単位のデータとして取り扱えるようになります。
    # 具体的には、request_text に格納されている文字列を ASCII エンコーディングを用いてバイト列に変換し、その結果を request_bytes という変数に格納しています。
    request_bytes = request_text.encode("ASCII")

    # write the byte sequence of a request to a socket.
    send_msg(client_socket, request_bytes)

    a = recv_msg(client_socket)

    # read the byte sequence of a response from a socket.
    # recv_msg 関数から受け取った複数のバイト列（バイトのリスト）を連結して、1 つのバイト列 received_bytes にまとめています。
    received_bytes = b''.join(a)

    # decode a byte sequence into a string.
    received_text = received_bytes.decode("ASCII")

    print(received_text)

    # close a socket that is no longer needed.
    client_socket.close()

if __name__ == "__main__":
    # execute the main function as the entry point of a script.
    main()





