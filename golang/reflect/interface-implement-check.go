package main

import (
	"fmt"
	"reflect"
)

type IT interface {
	test1()
}

type T struct {
	A string
}

func (t *T) test1() {}

func main() {
	t := &T{}
	ITF := reflect.TypeOf((*IT)(nil)).Elem()
	tv := reflect.TypeOf(t)
	fmt.Println(ITF)
	fmt.Println(tv)
	fmt.Println(tv.Implements(ITF))
}

