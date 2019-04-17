//https://flaviocopes.com/go-list-files/
package main

import (
    "fmt"
    "log"
    "os"
)

func main() {
    dirname := "."

    f, err := os.Open(dirname)
    if err != nil {
        log.Fatal(err)
    }
    files, err := f.Readdir(-1)
    f.Close()
    if err != nil {
        log.Fatal(err)
    }

    for _, file := range files {
        fmt.Println(file.Name())
    }
}

