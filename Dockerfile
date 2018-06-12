#docker build -t local/webserver-broker:v0.1.0 .
FROM golang:1.8

RUN go get github.com/golang/glog
RUN go get github.com/gorilla/mux
RUN go get github.com/kubernetes-incubator/service-catalog/contrib/pkg/broker/server
RUN go get github.com/kubernetes-incubator/service-catalog/contrib/pkg/broker/controller
RUN go get github.com/kubernetes-incubator/service-catalog/contrib/pkg/broker/user_provided/controller
RUN go get github.com/kubernetes-incubator/service-catalog/pkg

# RUN git clone https://github.com/kubernetes-incubator/service-catalog.git
ADD ./service-catalog /service-catalog
ADD ./charts/webserver-broker /service-catalog
ADD ./controller/controller.go /service-catalog/contrib/pkg/broker/user_provided/controller/controller.go

ADD ./image/webserver-broker.go /service-catalog/contrib/pkg/broker/server/server.go
ADD ./image/static /service-catalog/contrib/pkg/broker/server/static
ADD ./image/templates /service-catalog/contrib/pkg/broker/server/templates
ADD ./image/test /service-catalog/contrib/pkg/broker/server/test

WORKDIR /service-catalog

# RUN find $GOPATH -name "glog"
# to avoid error:
# panic: /tmp/go-build581983816/b001/exe/user-broker flag redefined: log_dir
RUN rm -rf /go/src/github.com/kubernetes-incubator/service-catalog/vendor/github.com/golang/glog

RUN GOOS=linux CGO_ENABLED=0 go build -a -ldflags '-w -s' -installsuffix cgo -o user-broker contrib/cmd/user-broker/user-broker.go
ENTRYPOINT [ "./user-broker" ]