package main

import (
    "fmt"
    "os"
    "bufio"
    "errors"
)

func tryDefer() {
    for i := 0; i < 100; i++ {
        defer fmt.Println(i)
        if i == 20 {
            panic("too many numbers printed")
        }
    }
}

func writeFile(filename string) {
    // file, err := os.Create(filename)
    file, err := os.OpenFile(filename, os.O_EXCL|os.O_CREATE,  0666)
    // err = errors.New("manually created error")
    if err != nil {
        if pathErr, ok := err.(*os.PathError); !ok {
            panic(err)
        } else {
            fmt.Printf("%s, %s, %s\n", pathErr.Op, pathErr.Path, pathErr.Err)
        }
    }
    defer file.Close()

    writer := bufio.NewWriter(file)
    defer writer.Flush()

    for i := 0; i < 100; i++ {
        fmt.Fprintln(writer, i)
    }
}

func main() {
    writeFile("1.txt")
    // tryDefer()
}
