package main

import (
	"fmt"
	"reflect"
)

type T struct {
	A int    `json:"aaa" test:"testaaa"`
	B string `json:"bbb" test:"testbbb"`
}

func main() {
	t := T{
		A: 123,
		B: "hello",
	}
	tt := reflect.TypeOf(t)
	fmt.Println(tt)
	for i := 0; i < tt.NumField(); i++ {
		field := tt.Field(i)
		if json, ok := field.Tag.Lookup("json"); ok {
			fmt.Println(json)
		}
		test := field.Tag.Get("test")
		fmt.Println(test)
	}
}
