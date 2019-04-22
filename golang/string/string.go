package main

import (
    "fmt"
    "unicode/utf8"
)

func main() {
    s := "zh大江东去！!"
    fmt.Println(s)
    fmt.Printf("%s\n", []byte(s))
    fmt.Printf("%X\n", []byte(s))
    for _, ch := range []byte(s) {
        fmt.Printf("%X ", ch)
    }
    fmt.Println()

    for id, ch := range s { // ch is a rune
        fmt.Printf("%d, %X; ", id, ch)
    }
    fmt.Println()

    fmt.Println(utf8.RuneCountInString(s))

    for id, ch := range []rune(s){
        fmt.Printf("%d, %X; ", id, ch)
    }

    fmt.Println()

    bytes := []byte(s)
    for len(bytes) > 0 {
        ch, size := utf8.DecodeRune(bytes)
        bytes = bytes[size:]
        fmt.Printf("%c ", ch)
    }

    fmt.Println()
}
