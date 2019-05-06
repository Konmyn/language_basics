#! /bin/bash
go test -bench . -cpuprofile cpu.out
go tool pprof cpu.out
# web # install graphviz
# quit
