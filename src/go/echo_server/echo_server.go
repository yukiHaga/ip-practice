package main

import (
	"fmt"
	"io"
	"log"
	"net"
	"time"
)

func main() {

	// net.Listenで以下のTCPネットワーク通信の手順を実行している。
	// 1. サーバー側のソケットの作成
	// 2. 利用するipアドレスとポートのバインド
	// 3. listenの実行
	// このメソッドを呼ぶと、実際にクライアントからの接続の待ち受けを開始します。
	ln, err := net.Listen("tcp", ":8080")
	if err != nil {
		fmt.Printf("failed to listen: %s\n", err.Error())
		return
	}

	for {
		log.Println("start")
		// このメソッドは、実際にクライアントから接続があったときに、それを処理するためのものです。
		// クライアントを表したコネクションを取得できる
		// クライアントへレスポンスを返した後、forのループが再度実行されて、ここの行で止まる
		clientConn, err := ln.Accept()
		// クライアントからコネクションの確立がリクエストされたら、以下の行が実行される。
		log.Println("after accept")
		if err != nil {
			fmt.Printf("failed to accept: %s\n", err.Error())
			return
		}

		go func() {
			// 実処理部分をgoroutineで別スレッド処理にする
			// go func() {
			// バッファはコンピュータで、データを一時的に記憶する場所っていう意味
			buf := make([]byte, 1024)
			receivedByteSequenceSize, err := clientConn.Read(buf)
			if err != nil {
				fmt.Printf("failed to read: %s\n", err.Error())
				return
			}

			time.Sleep(time.Second * 10)

			// 第二引数を第一引数にコピーする。だからコネクションに書き込んだってことか。
			// Copy は、src で EOF に達するかエラーが発生するまで、src から dst(コネクション) へコピーする。
			// だからCopyを使うと、EOFが呼ばれるまでプログラムが終了しない
			// io.Copy(serverConn, serverConn)

			fmt.Println(string(buf[:receivedByteSequenceSize]))

			// time.Sleep(time.Second * 3)

			io.WriteString(clientConn, string(buf[:receivedByteSequenceSize]))

			// 必要ないならコネクションをクローズする
			// pythonならソケットをクローズしていた
			clientConn.Close()
			// }()
		}()
	}
}
