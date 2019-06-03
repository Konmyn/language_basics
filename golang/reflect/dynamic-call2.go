package main

import (
	"fmt"
	"reflect"
)

type T struct{}

func main() {
	name := "Do"
	t := &T{}
	a := reflect.ValueOf(1111)
	b := reflect.ValueOf("world")
	in := []reflect.Value{a, b}
	reflect.ValueOf(t).MethodByName(name).Call(in)
}

func (t *T) Do(a int, b string) {
	fmt.Println("hello"+b, a)
}
