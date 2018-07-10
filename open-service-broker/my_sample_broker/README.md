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

# ClusterServiceClass
$ oc get clusterserviceclasses -o=custom-columns=NAME:.metadata.name,EXTERNAL\ NAME:.spec.externalName
NAME                                   EXTERNAL NAME
1111                                   test-service1
2222                                   test-service2

# ClusterServicePlans
$ oc get clusterserviceplans -o=custom-columns=NAME:.metadata.name,EXTERNAL\ NAME:.spec.externalName
NAME                                   EXTERNAL NAME
1111-1                                 small-plan
1111-2                                 medium-plan
2222-1                                 workspace-plan

# ServiceInstance
$ oc create namespace sample-ns
$ oc create -f serviceinstance_service1.yaml
oc delete -f serviceinstance_service1.yaml
$ oc get serviceinstances -n sample-ns samplebroker-instance -o yaml
oc delete serviceinstances -n sample-ns samplebroker-instance

# ServiceBinding
$ oc create -f servicebinding.yaml
$ oc get servicebindings -n sample-ns samplebroker-binding -o yaml
$ oc get secrets -n sample-ns
NAME                       TYPE                                  DATA      AGE
samplebroker-binding       Opaque                                0         2m

# Check

$ curl -v -H "X-Broker-API-Version: 2.13" http://username:password@samplebroker-service.samplebroker.svc.cluster.local:5050/v2/catalog
...
"dashboard_client":{"id":"d618a501-ddca-4b6b-a450-9b5016bb3446","redirect_uri":"https://github.com/michalswi/","secret":"secret1"}
...

# OR
# log in to openshift UI -> samplebroker -> Overview -> test-service2 -> link to Dashboards
$ curl -H "X-Broker-API-Version: 2.13" http://username:password@samplebroker-service.samplebroker.svc.cluster.local:5050/sample-service/d618a501-ddca-4b6b-a450-9b5016bb3446
{"get_instance_id":"d618a501-ddca-4b6b-a450-9b5016bb3446"}

$ curl -H "X-Broker-API-Version: 2.13" http://username:password@samplebroker-service.samplebroker.svc.cluster.local:5050/sample-service/dashboard/d618a501-ddca-4b6b-a450-9b5016bb3446
<!DOCTYPE html>
<html>
  <head>
    <title>Dashboard</title>
  </head>
  <br><body>
    Welcome in dashboard..
  </body>
</html>

$ curl -H "X-Broker-API-Version: 2.13" http://username:password@samplebroker-service.samplebroker.svc.cluster.local:5050/sample-service/d618a501-ddca-4b6b-a450-9b5016bb3446/test-service2-lpvz8-jjdvd
{"binding_id":"test-service2-lpvz8-jjdvd","instance_id":"d618a501-ddca-4b6b-a450-9b5016bb3446"}

# DELETE [in progress]
$ oc delete serviceinstances -n sample-ns samplebroker-instance
$ oc delete clusterservicebrokers samplebroker
```