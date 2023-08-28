package main

import (
	"fmt"
	"log"
	"net"
)

func main() {
	// net.Dialで以下のソケットを用いたネットワーク通信の以下の手順を実行している
	// 1. socketの作成
	// 2. 指定したIPアドレスのホスト内のアプリケーションのポートに接続するコネクションをはる。内部的に3-way-handshakeをしてくれている
	clientConn, err := net.Dial("tcp", "localhost:8081")
	if err != nil {
		log.Printf("fail to connection: %v", err)
		return
	}

	// \r: キャリッジリターン (Carriage Return) を表します。これはテキストのカーソルを行の先頭に移動する制御文字です。
	// \n: ラインフィード (Line Feed) を表します。これはテキストのカーソルを次の行に移動する制御文字です。
	// HTTPのプロトコルでは、HTTPリクエストメッセージはリクエストライン、ヘッダー部、ボディ部で構成されていて、かつヘッダー部とボディ部は空行で区切られている。
	// \r\nだと１回改行するだけでカーソル自体はその行にいる。つまり空行を作らない。そのため、さらに改行することで空行を作っている。
	// 以下ではリクエストラインしか書いてない
	request_text := "GET / HTTP/1.0\r\n\r\n"

	// request_textをバイト列にキャストして、クライアントのソケットが作ったコネクションに書き込んでいる
	_, err = clientConn.Write([]byte(request_text))
	if err != nil {
		log.Printf("fail to Write to connection: %v", err)
		return
	}

	// バイト列が格納される
	// 1024バイトある
	buf := make([]byte, 1024)
	fmt.Println(buf)
	// Readはコネクションからデータを読み込む
	// おそらくReadの内部でチャンクを何回も受け取って、それをbufに格納していると思う
	receivedByteSequenceSize, err := clientConn.Read(buf)
	if err != nil {
		log.Printf("fail to Read connection: %v", err)
		return
	}

	fmt.Println(buf)
	fmt.Println(string(buf))
	fmt.Println(receivedByteSequenceSize)
	fmt.Println(buf[:receivedByteSequenceSize])
	fmt.Println(len(buf[:receivedByteSequenceSize]))
	fmt.Println(string(buf[:receivedByteSequenceSize]))
}
