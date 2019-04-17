package main

import (
    "fmt"
)

func main() {
    const (
        python = iota
        java
        _
        c
        cpp
        javascript
    )
    fmt.Println(python, java, c, cpp, javascript)

    const (
        b = 1 << (10 * iota)
        kb
        mb
        gb
        tb
        pb
    )

    fmt.Println(b, kb, mb, gb, tb, pb)
}
