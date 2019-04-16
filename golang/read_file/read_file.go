package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	file, err := os.Open("words.txt")
	if err != nil {
		fmt.Println(nil)
		os.Exit(1)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		fmt.Println(strings.TrimSpace(scanner.Text()))
	}

}
