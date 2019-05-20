package main

import (
	"fmt"
	"time"
)

func routine(i int, sigChan chan int){
	select {
	case k, ok := <-sigChan:
		fmt.Printf("get info from %d\n", i)
		fmt.Println(i, k, ok)
	}
}

func main() {
	intChan := make(chan int)
	for i := 0; i < 5; i++ {
		go routine(i, intChan)
	}
	intChan <- 99
	close(intChan)
	time.Sleep(time.Second)
}