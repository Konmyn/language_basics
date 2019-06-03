// https://segmentfault.com/a/1190000016230264
package main

import (
	"fmt"
	"reflect"
)

type T struct{}

func main() {
	name := "Do"
	t := &T{}
	reflect.ValueOf(t).MethodByName(name).Call(nil)
	// same as
	t.Do()
}

func (t *T) Do() {
	fmt.Println("hello")
}