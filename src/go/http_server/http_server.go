package main

import (
	"fmt"
	"net/http"
	"os"
)

func main() {
	err := http.ListenAndServe(":8081", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		b, err := os.ReadFile("../../index.html")
		if err != nil {
			fmt.Printf("failed to read file: %s\n", err.Error())
		}
		fmt.Fprintln(w, string(b))
	}))

	if err != nil {
		fmt.Printf("failed to terminate server: %s\n", err.Error())
		os.Exit(1)
	}
}
