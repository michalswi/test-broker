### Sample Test Service Broker

**Test broker deployment in openshift.**  
How to deploy openshift you can find [here](https://github.com/gshipley/installcentos).  

Dictionary:
- **CATALOG** - return service information including related service plans,
- **PROVISION** - allocation of new resources = CREATE THE SERVICE (add it to catalog),
- **DEPROVISION** - removal of resources created by the provisioning action = DELETE THE SERVICE (remove it from the catalog),
- **BIND** - create resources to allow applications to communicate with the provisioned resources = BIND/LINK a service to an app,
- **UNBIND** - removal of resources created by the binding action = REMOVE the linkage to an app.

**To start**  
```sh
$ oc login -u <user> -p <pass> https://console.test.localhost:8443/

$ oc new-project samplebroker --description="Sample broker project" --display-name="samplebroker"

$ oc project samplebroker

$ oc create namespace samplebroker

$ oc create -f templates/secret.yaml
#OR:
oc create secret generic test-secret --from-literal=username=username --from-literal=password=password --namespace samplebroker
```

**Launch service-broker using Openshift-cli**
```sh
$ oc create -f templates/sampleBroker.yaml

# pod & service should be available
```

**Launch service-broker using Templates**
```sh
$ oc create -f servicebrokertemplate.yaml 

$ oc describe template samplebroker-template
oc get template samplebroker-template -o yaml
oc delete template 

# log in to openshift UI -> Select from Project -> select 'samplebroker' project -> Add to project -> Select from Project -> select 'samplebroker-template'
#OR
# log in to openshift UI -> Select from Project -> select 'samplebroker' project -> Catalog -> Other -> select 'samplebroker-template'

# pod & service should be available
```

**Next steps** are the same for CLI's and template's way
```sh
$ oc get services samplebroker-service
oc get services samplebroker-service -o yaml
oc describe service sample-broker-service

$ oc create -f templates/clusterservicebroker.yaml

$ oc get clusterservicebrokers samplebroker -o yaml
# if 'Successfully fetched catalog entries from broker.' 
# you should see two services available: test-service1 & test-service2
oc delete clusterservicebrokers samplebroker

[in progress..]
```