package main

import (
    "fmt"
    "strconv"
    "os"
    "bufio"
)

func main() {
    fmt.Println(
    intToBin(2),
    intToBin(20),
    intToBin(1024),
    )
    const filename = "abc.txt"
    printFile(filename)

    foreverRun()
}

func intToBin(a int) string {
    if a == 0 {
        return "0"
    }
    r := ""
    for ; a > 0; a /= 2 {
        r = strconv.Itoa(a % 2) + r
    }
    return r
}

func printFile(f string) {
    file, err := os.Open(f)
    defer file.Close()
    if err != nil {
        panic(err)
    }

    scanner := bufio.NewScanner(file)

    for scanner.Scan() {
        fmt.Println(scanner.Text())
    }
}

func foreverRun() {
    for {
        fmt.Println("hello")
    }
}
