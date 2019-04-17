package main

import (
    "fmt"
    "io/ioutil"
)

func main() {
    const filename = "abc.txt"
    if content, err := ioutil.ReadFile(filename); err != nil {
        fmt.Println(err)
    } else {
        fmt.Printf("%s\n", content)
    }

    fmt.Println(
        grade(50),
        grade(60),
        grade(70),
        grade(90),
        grade(90),
        grade(-90),
    )
}

func grade(score int) string {
    g := ""
    switch {
    case score < 0 || score > 100:
        panic(fmt.Sprintf("wrong score %d", score))
    case score < 60:
        g = "E"
    case score < 70:
        g = "D"
    case score < 80:
        g = "C"
    case score < 90:
        g = "B"
    case score <= 100:
        g = "A"
    }
    return g
}
