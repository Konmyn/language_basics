package main

import(
    "fmt"
    //"errors"
)

func recoverPanic() {
    defer func() {
        err := recover()
        if r, ok := err.(error); ok {
            fmt.Println("error occured: ", r)
        } else {
            panic(fmt.Sprintf("i don't know what to do: %v", err))
        }
    }()

    // panic(errors.New("paniced errors"))
    panic(123)
    // a := 0
    // b := 5/a
    // fmt.Println(b)

}

func main() {
    recoverPanic()
}
