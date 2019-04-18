package main

import (
    "fmt"
)

func main() {
    var arr1 [5]int
    arr2 := [5]int{9, 7, 2, 8, 5}
    arr3 := [...]int{2, 2, 2, 2, 2, 2, 2}
    var grid [3][4]int
    fmt.Println(arr1, arr2, arr3)
    fmt.Println(grid)

    for i := 0; i < len(arr2); i++ {
        fmt.Println(arr2[i])
    }

    for i := range arr3 {
        fmt.Println(i)
    }

    for i, v := range arr3 {
        fmt.Println(i, v)
    }

    for _, v := range arr3 {
        fmt.Println(v)
    }

    printArray(arr2)
    fmt.Println(arr2)
    pprintArray(&arr2)
    fmt.Println(arr2)
}

func printArray(a [5]int){
    a[0] = 100
    for _, v := range a {
        fmt.Println(v)
    }
}

func pprintArray(a *[5]int){
    a[0] = 100 // attention, same as (*a), and you cannot use *a[0]
    for _, v := range a { // attention, same as *a
        fmt.Println(v)
    }
}
