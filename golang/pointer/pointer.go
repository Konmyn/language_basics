package main

import (
    "fmt"
)

func swap(a, b *int) {
    *a, *b = *b, *a
}

func swap_wrong(a, b *int) {
    fmt.Println(a, b)
    fmt.Println(*a, *b)
    a, b = b, a
    fmt.Println(a, b)
    fmt.Println(*a, *b)
}

func swap_tradition(a, b int) (int, int) {
    return b, a
}

func main() {
    a, b := 1, 2
    fmt.Println("before: ", a, b)
    swap(&a, &b)
    fmt.Println(a, b)
    swap_wrong(&a, &b)
    fmt.Println(a, b)
    a, b = swap_tradition(a, b)
    fmt.Println(a, b)
}
