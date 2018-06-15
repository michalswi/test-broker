### Test Open Service Broker

Open Broker API repo is [here](https://github.com/eruvanos/openbrokerapi).  

OB API python code is [here](https://pypi.org/project/openbrokerapi/).  

OB API details are [here](http://openbrokerapi.readthedocs.io/en/latest/openbrokerapi.html).  

Templates are [here](./templates).  

Run deployment:  
```sh
$ kubectl create namespace testbroker
$ kubectl create -f templates/testBroker.yaml
```

Local tests, more details [here](https://github.com/openservicebrokerapi/servicebroker/blob/v2.12/spec.md#request):  
```sh
$ docker run -d -p 8080:5000 local/run-broker:v0.1.0
$ curl -v -H "X-Broker-API-Version: 2.12" http://user:pass@localhost:8080/v2/catalog
...
HTTP/1.0 412 PRECONDITION FAILED
$ curl -v -H "X-Broker-API-Version: 2.13" http://user:pass@localhost:8080/v2/catalog
...
{"services":[{"bindable":true,"description":"Example Service does nothing"
```
More about Headers and API version [here](https://github.com/openservicebrokerapi/servicebroker/blob/v2.13/spec.md#api-version-header).