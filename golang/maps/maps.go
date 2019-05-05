package main

import (
    "fmt"
)

func main(){
    m := map[string]int{
        "python": 1,
        "c": 2,
        "java": 3,
        "go": 4,
        "c++": 5,
        "c#": 6,
    }

    m2 := make(map[string]string) // m2 == empty map

    var m3 map[string]int // m3 == nil

    fmt.Println(m, m2, m3)

    fmt.Println("traversing map")
    for k, v := range m {
        fmt.Println(k, v)
    }

    score_python, in := m["python"]
    fmt.Println(score_python, in)
    score_perl, in := m["perl"]
    fmt.Println(score_perl, in)

    delete(m, "python")

    score_python, in = m["python"]
    fmt.Println(score_python, in)

    fmt.Println(maxLenOfNonRepeatSubstr(""))
    fmt.Println(maxLenOfNonRepeatSubstr("abcdefg"))
    fmt.Println(maxLenOfNonRepeatSubstr("abccba"))
    fmt.Println(maxLenOfNonRepeatSubstr("123ssww"))
    fmt.Println(maxLenOfNonRepeatSubstr("s"))
    fmt.Println(maxLenOfNonRepeatSubstr("yyyyyyyyyyyyyyyy"))
    fmt.Println(maxLenOfNonRepeatSubstr("中国国中"))
    fmt.Println(maxLenOfNonRepeatSubstr("这里是慕课网"))
}

func maxLenOfNonRepeatSubstr(s string) int {
    maxLen := 0
    start := 0
    lastOccured := make(map[rune]int)
    for id, ch := range []rune(s){
        if loc, in := lastOccured[ch]; in && loc >= start {
            start = id + 1
        }
        if id - start + 1 > maxLen {
            maxLen = id - start + 1
        }
        lastOccured[ch] = id
    }
    return maxLen
}
