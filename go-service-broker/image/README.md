```sh
$ cd image/
$ tree .
.
├── README.md
├── static
│   ├── images
│   │   └── nokia.png
│   ├── static.html
│   └── styles
│       └── style.css
├── templates
│   └── index.html
├── test
│   └── test.html
├── webserver-broker.go
└── webserver.go
$ go run webserver.go <port_number>
```