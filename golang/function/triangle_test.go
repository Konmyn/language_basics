package main

import (
    "testing"
)

func TestTriangle(t *testing.T) {
    test := []struct {a, b, c int} {
        {3, 4, 5},
        {4, 5, 0},
        {4, 9, 0},
        {5, 12, 13},
        {8, 15, 17},
        {12, 35, 37},
        {30000, 40000, 50000},
    }
    for _, i := range test {
        if result := calcTriangle(i.a, i.b); result != i.c {
            t.Errorf("calcTriangle(%d, %d); " +
            "got %d; excepted %d", i.a, i.b, result, i.c)
        }
    }
}
