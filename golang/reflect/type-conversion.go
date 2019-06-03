package main

import (
	"fmt"
	"reflect"
)

type T struct {
	A int    `newT:"AA"`
	B string `newT:"BB"`
}

type newT struct {
	AA int
	BB string
}

func main() {
	t := T{
		A: 123,
		B: "hello",
	}
	tt := reflect.TypeOf(t)
	tv := reflect.ValueOf(t)
	fmt.Println(tt)
	fmt.Println(tv)

	newT := &newT{}
	newTValue := reflect.ValueOf(newT)
	fmt.Println(newT)
	fmt.Println(newTValue)

	for i := 0; i < tt.NumField(); i++ {
		field := tt.Field(i)
		newTTag := field.Tag.Get("newT")
		tValue := tv.Field(i)
		newTValue.Elem().FieldByName(newTTag).Set(tValue)
	}

	fmt.Println(newT)
}

