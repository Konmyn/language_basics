package main

import (
    "testing"
)

func TestNonRepeating(t *testing.T) {
    test := []struct{
        s string
        a int
    } {
        // normal cases
        {"abcdefg", 7},
        {"abccba", 3},
        {"123ssww", 4},

        // edge cases
        {"s", 1},
        {"", 0},
        {"abcabcabcabcd", 4},
        {"yyyyyyyyyyyyyyyy", 1},

        // chinese support
        {"中国国中", 2},
        {"这里是慕课网", 6},
    }
    for _, i := range test {
        if l := maxLenOfNonRepeatSubstr(i.s); l != i.a {
            t.Errorf("maxLenOfNonRepeatSubstr(%s); got %d; expection %d", i.s, l, i.a)
        }
    }
}

func BenchmarkNonRepeating(b *testing.B) {
    s := "abcabcabcabcabcabcabcabcabcabcd"
    a := 4
    for i := 0; i < b.N; i++ {
        if l := maxLenOfNonRepeatSubstr(s); l != a {
            b.Errorf("maxLenOfNonRepeatSubstr(%s); got %d; expection %d", s, l, a)
        }
    }
}
