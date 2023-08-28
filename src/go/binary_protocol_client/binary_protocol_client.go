package main

import (
	"encoding/binary"
	"fmt"
	"log"
	"net"
)

func main() {
	clientConn, err := net.Dial("tcp", ":8080")
	if err != nil {
		log.Printf("fail to connection: %v", err)
		return
	}

	operand1, operand2 := int32(1000), int32(2000)

	requestByteSequence := make([]byte, 1024)
	// binary.BigEndian.PutUint32関数を使用してint32の値をビッグエンディアンのバイト列に変換しています。
	// 最後の場合はn-1
	binary.BigEndian.PutUint32(requestByteSequence[:4], uint32(operand1))
	// 最初の場合はn
	binary.BigEndian.PutUint32(requestByteSequence[4:], uint32(operand2))

	_, err = clientConn.Write(requestByteSequence)
	if err != nil {
		log.Printf("fail to Write to connection: %v", err)
		return
	}

	buf := make([]byte, 1024)
	receivedByteSequenceSize, err := clientConn.Read(buf)
	if err != nil {
		log.Printf("fail to Read connection: %v", err)
		return
	}

	result := binary.BigEndian.Uint64(buf[:receivedByteSequenceSize])
	fmt.Printf("result: %v\n", result)
	clientConn.Close()
}
