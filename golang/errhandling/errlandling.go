package main

import (
    "os"
    "net/http"
    "log"

    listing "github.com/Konmyn/language_basics/golang/errhandling/filelisting"
)

type HandlFunc func(http.ResponseWriter, *http.Request) error

func ErrHandler(h HandlFunc) func(http.ResponseWriter, *http.Request) {
    return func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if r := recover(); r != nil {
                log.Printf("panic: %v", r)
                http.Error(w, http.StatusText(http.StatusInternalServerError), http.StatusInternalServerError)
            }
        }()
        err := h(w, r)
        if err != nil {
            log.Printf("error occurred handling request: %s", err.Error())

            if ur, ok := err.(userError); ok {
                http.Error(w, ur.Message(), http.StatusBadRequest)
                return
            }

            code := http.StatusOK
            switch {
            case os.IsNotExist(err):
                code = http.StatusNotFound
            case os.IsPermission(err):
                code = http.StatusForbidden
            default:
                code = http.StatusInternalServerError
            }
            http.Error(w, http.StatusText(code), code)
        }
    }
}

type userError interface {
    error
    Message() string
}

func main() {
    http.HandleFunc("/", ErrHandler(listing.FileReader))

    err := http.ListenAndServe("0.0.0.0:8080", nil)
    if err != nil {
        panic(err)
    }
}
