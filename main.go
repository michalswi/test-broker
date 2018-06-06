//
// https://github.com/prydonius/mariadb-broker/blob/master/main.go

package main

import (
	"flag"
	"fmt"
	"os"
	"path"

	"./controller"

	// there is no server.Start in github...server
	// "github.com/kubernetes-incubator/service-catalog/contrib/pkg/broker/server"
	"./broker"

	"github.com/kubernetes-incubator/service-catalog/pkg"
)

var options struct {
	Port int
}

func init() {
	flag.IntVar(&options.Port, "port", 8005, "use '--port' option to specify the port for broker to listen on")
	flag.Parse()
}

func main() {
	if flag.Arg(0) == "version" {
		fmt.Printf("%s/%s\n", path.Base(os.Args[0]), pkg.VERSION)
		return
	}

	server.Start(options.Port, controller.CreateController())
}
