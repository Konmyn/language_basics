package main

import (
    "fmt"
    "io"
    "strings"
    "bufio"
)

type Adder func(int) int

func adder() Adder {
    sum := 0
    return func(v int) int {
        sum += v
        return sum
    }
}

type iAdder func(int) (int, iAdder)

func adder2 (base int) iAdder {
    return func(v int) (int, iAdder) {
        return base + v, adder2(base+v)
    }
}

func fibonacci() fibGen {
    a, b := 0, 1
    return func() int {
        a, b = b, a+b
        return a
    }
}

type fibGen func() int

func (f fibGen) Read(p []byte) (n int, err error) {
    next := f()
    if next > 10000 {
        return 0, io.EOF
    }
    s := fmt.Sprintf("%d\n", next)

    // TODO incorrect if p is too small
    return strings.NewReader(s).Read(p)
}

func printFileContents(reader io.Reader) {
    scanner := bufio.NewScanner(reader)
    for scanner.Scan() {
        fmt.Println(scanner.Text())
    }
}

func main() {
    a := adder()
    for i := 0; i < 10; i++ {
        fmt.Printf("0+1+...+%d=%d\n", i, a(i))
    }

    b := adder2(0)
    for j := 0; j < 10; j++ {
        var r int
        r, b = b(j)
        fmt.Printf("0+1+...+%d=%d\n", j, r)
    }
    f := fibonacci()
    fmt.Println(f())
    fmt.Println(f())
    fmt.Println(f())
    fmt.Println(f())
    fmt.Println(f())
    fmt.Println(f())
    fmt.Println(f())
    fmt.Println(f())
    fmt.Println(f())
    fmt.Println(f())
    fmt.Println(f())

    nf := fibonacci()

    printFileContents(nf)
}
