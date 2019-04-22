package main

import (
    "fmt"
)

func main() {
    arr := [...]int{0, 1, 2, 3, 4, 5, 6, 7, 8}
    fmt.Println("arr[2:6]", arr[2:6])
    fmt.Println("arr[2:]", arr[2:])
    fmt.Println("arr[:6]", arr[:6])
    fmt.Println("arr[:]", arr[:])

    s1 := arr[5:7]
    fmt.Println("s1:", s1)
    s2 := append(s1, 14)
    s3 := append(s2, 15)
    s4 := append(s3, 16)
    fmt.Println("arr", arr)
    fmt.Println("s4", s4)
    fmt.Printf("len(s4): %d, cap(s4): %d\n", len(s4), cap(s4))

    var s []int
    for i := 0; i < 10; i++ {
        fmt.Printf("len(s): %d, cap(s): %d\n", len(s), cap(s))
        s = append(s, i)
    }
    fmt.Println(s)

    ss1 := []int{2, 4, 6, 8}
    ss2 := make([]int, 16) // len(s2) = 16
    ss3 := make([]int, 10, 32) // len(s3) = 10, cap(32) = 32
    fmt.Println(ss1)
    fmt.Println(ss2)
    fmt.Println(ss3)

    copy(ss2, ss1)
    fmt.Println(ss2)

    // deleting elements from slice
    ss2 = append(ss2[:3], ss2[4:]...)
    fmt.Println(ss2)

    // pop from front
    front := ss2[0]
    ss2 = ss2[1:]

    fmt.Println(ss2)

    // pop from tail
    tail := ss2[len(ss2)-1]
    ss2 = ss2[:len(ss2)-1]
    fmt.Println(front, tail)
    fmt.Println(ss2)
}
