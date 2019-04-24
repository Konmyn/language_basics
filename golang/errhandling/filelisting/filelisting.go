package listing

import (
	"io/ioutil"
	"net/http"
	"os"
	"log"
	"strings"
)

const prefix = "/list/"

type userError string

func (u userError) Error() string {
	return u.Message()
}

func (u userError) Message() string {
	return string(u)
}

func FileReader(w http.ResponseWriter, r *http.Request) error {
	if strings.Index(r.URL.Path, prefix) != 0 {
		return userError("url must start with: " + prefix)
	}
	path := r.URL.Path[len(prefix):]
	log.Printf("accessing: %s", path)
	file, err := os.Open(path)
	if err != nil {
		return err
	}
	defer file.Close()

	all, err := ioutil.ReadAll(file)
	if err != nil {
		return err
	}

	w.Write(all)
	return nil
}
