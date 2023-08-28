package main

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"log"
	"net"
)

func main() {
	ln, err := net.Listen("tcp", ":8080")
	if err != nil {
		log.Printf("fail to listen: %v\n", err)
		return
	}

	for {
		clientConn, err := ln.Accept()
		if err != nil {
			log.Printf("fail to accept: %v\n", err)
			return
		}

		buf := make([]byte, 1024)

		_, err = clientConn.Read(buf)
		if err != nil {
			log.Printf("fail to read conn: %v\n", err)
			return
		}

		var operand1, operand2 int32

		reader := bytes.NewReader(buf)

		// Readは構造化バイナリ・データをrからdataに読み込む。
		// dataは固定サイズ値へのポインタか、固定サイズ値のスライスでなければならない。
		// rから読み込まれたバイトは、指定されたバイト順序でデコードされ、dataの連続するフィールドに書き込まれる。
		// operand1がint32だから、32ビット分しか書き込まれないはず。
		err = binary.Read(reader, binary.BigEndian, &operand1)
		if err != nil {
			fmt.Println("Error reading operand1:", err)
			return
		}
		fmt.Printf("operand1: %v\n", operand1)

		err = binary.Read(reader, binary.BigEndian, &operand2)
		if err != nil {
			fmt.Println("Error reading operand2:", err)
			return
		}
		fmt.Printf("operand2: %v\n", operand2)

		result := operand1 + operand2

		// ホストバイトオーダー(macOSの場合リトルエンディアン)のバイト列をネットワークバイトオーダー(tcpの場合ビッグエンディアン)のバイト列に変換する
		responseByteSequence := make([]byte, 1024)
		// binary.BigEndian.PutUint32関数を使用してint32の値をビッグエンディアンのバイト列に変換しています。
		binary.BigEndian.PutUint64(responseByteSequence, uint64(result))

		clientConn.Write(responseByteSequence)
		clientConn.Close()
	}
}
