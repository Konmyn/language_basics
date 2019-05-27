package main

import (
	flag "github.com/spf13/pflag"
)

func main(){
	flags := flag.NewFlagSet("run", flag.ExitOnError)
	flags.BoolP("verbose", "v", false, "verbose output")
	flags.String("coolflag", "yeaah", "it's really cool flag")
	flags.Int("usefulflag", 777, "sometimes it's very useful")
	flags.SortFlags = false
	flags.PrintDefaults()
}
