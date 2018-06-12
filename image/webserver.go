package main

import (
	"fmt"
	"net/http"
	"os"
	"path"
	"strconv"
)

// handling /v2/config...:
// https://github.com/kubernetes-incubator/service-catalog/blob/master/contrib/pkg/broker/server/server.go

// user-broker.go
// https://github.com/kubernetes-incubator/service-catalog/blob/master/contrib/cmd/user-broker/user-broker.go

func main() {

	if os.Args != nil && len(os.Args) > 1 {
		port := os.Args[1]
		fmt.Println("started..")
		if IsNumeric(port) {
			if IsValidPort(port) {
				http.HandleFunc("/hello", helloHandler)
				fs := http.FileServer(http.Dir("./static"))
				http.Handle("/file/", http.StripPrefix("/file/", fs))
				http.HandleFunc("/", homePageTemplate)
				http.ListenAndServe(":"+port, nil)
			}
		} else {
			fmt.Println("Only digits are valid..")
		}
	} else {
		fmt.Println("Missing port number..")
	}
}

func IsNumeric(s string) bool {
	_, err := strconv.ParseFloat(s, 64)
	return err == nil
}

func IsValidPort(s string) bool {
	i2, err := strconv.ParseInt(s, 10, 64)
	var status bool
	status = false
	if err == nil {
		if i2 > 0 && i2 < 65535 {
			status = true
		} else {
			fmt.Println("Wrong port number..")
		}
	}
	return status
}

func helloHandler(w http.ResponseWriter, req *http.Request) {
	fmt.Fprintf(w, "%s", "Hello world \n")
	getOut := reqHandler(req)
	fmt.Println(getOut)
}

func homePage(w http.ResponseWriter, req *http.Request) {
	fmt.Fprintf(w, "%s", "Home Page.. \n")
	getOut := reqHandler(req)
	fmt.Println(getOut)
}

func homePageTemplate(w http.ResponseWriter, req *http.Request) {

	root := "templates"
	if req.URL.Path == "" || req.URL.Path == "/" {
		http.ServeFile(w, req, path.Join(root, "index.html"))
	} else {
		http.ServeFile(w, req, path.Join(root, req.URL.Path))
	}

	getOut := reqHandler(req)
	fmt.Println(getOut)
}

func getTest(w http.ResponseWriter, req *http.Request) {
	getOut := reqHandler(req)
	fmt.Println(getOut)
}

func reqHandler(req *http.Request) []string {
	var keys []string
	url := fmt.Sprintf("%v %v %v", req.Method, req.URL, req.Proto)
	keys = append(keys, url)
	keys = append(keys, fmt.Sprintf("Host: %v", req.Host))
	return keys
}
