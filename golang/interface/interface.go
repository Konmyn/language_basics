package main

import (
    "fmt"
    "time"
    "net/http"
    "net/http/httputil"
)

type retriver interface {
    Get(url string) string
}

func download(r retriver) string {
    return r.Get("http://www.baidu.com")
}

func main() {
    var r retriver
    var t retriver
    r = retri{"this is a fake retriver"}
    //r = &retri{"this is a fake retriver"} // this is also ok
    t = &realretri{
        UserAgent: "golang",
        TimeOut: time.Minute,
    }
    inspect(r)
    inspect(t)

    // type assertion
    re := t.(*realretri)
    fmt.Println(re.TimeOut)

    rr, ok := r.(retri)
    fmt.Println(rr, ok)

    //fmt.Println(download(r))
    //fmt.Println(download(t))

    a := []interface{}{1, 2, nil, "abc", "123", "中国"}
    fmt.Println(a)
}

type retri struct {
    Content string
}

func (r retri) Get(url string) string {
    return r.Content
}

type realretri struct {
    UserAgent string
    TimeOut time.Duration
}

func (r *realretri) Get (url string) string {
    resp, err := http.Get(url)
    if err != nil {
        panic(err)
    }

    result, err := httputil.DumpResponse(resp, true)
    defer resp.Body.Close()

    if err != nil {
        panic(err)
    }

    return string(result)
}

func inspect(r retriver) {
    fmt.Printf("%T, %v\n", r, r)
    fmt.Println("type switch:")
    switch v := r.(type){
    case retri:
        fmt.Printf("mock content: %s\n", v.Content)
    case *realretri:
        fmt.Println("user agent: ", v.UserAgent)
    }

}
