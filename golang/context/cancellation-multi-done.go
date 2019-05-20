package main

import (
	"context"
	"fmt"
	"time"
)
func operation(i int, stopCh <-chan struct{}) error {
	fmt.Printf("runing in %d\n", i)
	select {
	case <-stopCh:
		fmt.Printf("stopping %d\n", i)
		return nil
	}
}

func main() {
	// Create a new context
	ctx := context.Background()
	// Create a new context, with its cancellation function
	// from the original context
	ctx, cancel := context.WithCancel(ctx)

	// Run two operations: one in a different go routine
	for i := 0; i < 5; i++ {
		go operation(i, ctx.Done())
	}

	cancel()

	time.Sleep(time.Second)
}

