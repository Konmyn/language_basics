package main

import (
	"fmt"
	"reflect"
)

func main() {
	a := 1
	t := reflect.TypeOf(a)
	switch t.Kind() {
	case reflect.Int:
		fmt.Println("int")
	case reflect.String:
		fmt.Println("string")
	}
}

