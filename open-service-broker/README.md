### Test Open Service Broker

Python implementation of Open Service Broker API repo is [here](https://github.com/eruvanos/openbrokerapi).  

OSB API python code is [here](https://pypi.org/project/openbrokerapi/).  

OSB API details are [here](http://openbrokerapi.readthedocs.io/en/latest/openbrokerapi.html). 

OSB API checker is [here](https://github.com/openservicebrokerapi/osb-checker).  

Templates for kubernetes are [here](./templates).  

**Local tests**, more details are [here](https://github.com/openservicebrokerapi/servicebroker/blob/v2.13/spec.md#request).    
```sh
$ docker build -t local/run-broker:v0.1.0 .
$ docker run -d -p 5050:5000 local/run-broker:v0.1.0
$ curl -v -H "X-Broker-API-Version: 2.12" http://user:pass@localhost:5050/v2/catalog
...
HTTP/1.0 412 PRECONDITION FAILED
$ curl -v -H "X-Broker-API-Version: 2.13" http://user:pass@localhost:5050/v2/catalog
...
{"services":[{"bindable":true,"description":"Example Service does nothing"
```
More about Headers and API version [here](https://github.com/openservicebrokerapi/servicebroker/blob/v2.13/spec.md#api-version-header).

**Kubernetes tests**  
Run deployment:  
```sh
$ kubectl create namespace testbroker

# if you have your own user/password add these values to templates/secret.yaml
# https://kubernetes.io/docs/concepts/configuration/secret/

$ echo -n 'username' | base64
dXNlcm5hbWU=
$ echo -n 'password' | base64
cGFzc3dvcmQ=

$ kubect create -f templates/secret.yaml
$ kubectl create -f templates/testBroker.yaml
```

Check:  
```sh
$ kubectl exec -n testbroker testbroker-deployment-7bc4ffd5c-lqc9p -- cat /etc/resolv.conf
nameserver 10.10.0.3
search testbroker.svc.cluster.local svc.cluster.local cluster.local
options ndots:5
$ curl -v -H "X-Broker-API-Version: 2.13" http://username:password@testbroker-service.testbroker.svc.cluster.local:5050/v2/catalog
```