package main

import (
    "fmt"
    "math/cmplx"
    "math"
)

func main() {
    r := cmplx.Exp(1i*math.Pi)+1
    fmt.Println(r)
    fmt.Printf("%.3f\n", r)
}
