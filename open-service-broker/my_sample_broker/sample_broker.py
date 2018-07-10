#!/usr/bin/env python

# base on that examples:
# https://www.altoros.com/blog/creating-a-sample-service-broker-for-cloud-foundry-with-pythons-flask/
# https://github.com/IBM-Cloud/Bluemix-ServiceBroker/blob/master/bmx-sample-broker.py

import os
from flask import Flask, jsonify, request, abort, Response, make_response, render_template
# https://stackoverflow.com/questions/308999/what-does-functools-wraps-do
from functools import wraps
from sample_health_check import health_check
import uuid
import logging

logging.basicConfig()
logger = logging.getLogger("ServiceBrokerRegistrator")
logger.setLevel(logging.INFO)

app = Flask(__name__)
app.register_blueprint(health_check)

service_port = os.getenv('PORT', '5000')
service_host = 'localhost'

#-------------------
# https://github.com/openservicebrokerapi/servicebroker/blob/v2.13/spec.md#api-version-header
X_BROKER_API_MAJOR_VERSION = 2
X_BROKER_API_MINOR_VERSION = 13
X_BROKER_API_VERSION_NAME = 'X-Broker-Api-Version'

#-------------------
# Service Endpoints (will be replaced with Workspaces endpoints)

service_instance = "http://{}:{}/sample-service/".format(service_host, service_port)
service_dashboard = "http://{}:{}/sample-service/dashboard/".format(service_host, service_port)

#-------------------
# Plans related to ClusterServicePlan
# IF only ONE service_plan per service there won't be PLAN when selecting INFORMATION -> CONFIGURATION
service_plan11 = {
    "id": "1111-1",
    "name": "small-plan",
    "description": "Sample small plan description",
    "free": True
}

service_plan12 = {
    "id": "1111-2",
    "name": "medium-plan",
    "description": "Sample medium plan description",
    "free": True,
    "metadata": {}   
}

# uuid 
# -> https://stackoverflow.com/questions/20342058/which-uuid-version-to-use
# -> https://stackoverflow.com/questions/10867405/generating-v5-uuid-what-is-name-and-namespace
# "id": "{}".format(uuid.uuid4()),  ---> if openshift instance will be restared new uuid will be generated..
# solution could be use uuid3 or uuid5

# schemas
# https://github.com/openservicebrokerapi/servicebroker/blob/master/spec.md#schemas-object
# https://apidocs.cloudfoundry.org/2.1.0/service_plans/list_all_service_plans.html
# https://github.com/kubernetes-incubator/service-catalog/blob/master/contrib/pkg/broker/user_provided/controller/controller.go

service_plan21 = {
    "id": "2222-1",
    "name": "workspace-plan",
    "description": "Service plan description",
    "free": True,
    "schemas": {
        "service_instance": { 
            "create": {
                "parameters": {
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "type": "object",
                    "properties": {
                        "MySpace" :{
                            "name": "MYSPACE",
                            "description": "The OpenShift TestSpace",
                            "value": "openshift",
                            "type": "string"
                        },
                        "Test" :{
                            "name": "TEST",
                            "description": "Test test",
                            "value": "",
                            "type": "string",
                            "required": True
                        }                        
                    }
                }
            },
            "update": {}
        },
        "service_binding": {
            "create": {}
        }
    }    
}

# Services related to ClusterServiceClass
service1 = {
    'id': '1111',
    'name': 'test-service1',
    'description': 'Example service',
    'bindable': True,
    'plans': [service_plan11, service_plan12]
}

service2 = {
    'id': '2222',
    'name': 'test-service2',
    'description': 'Service to test Workspaces API',
    'bindable': True,
    'tags': ['private', 'workspace'], 
    'plans': [service_plan21],
    'metadata' : {
        'displayName': 'test-service2',
        'longDescription': 'Service description',
        'providerDisplayName': 'michalswi', 
        'documentationUrl': 'https://github.com/openservicebrokerapi/servicebroker/blob/v2.13/spec.md',
        'supportUrl': 'https://github.com/michalswi/test-broker/issues'
    },    
    'dashboard_client': {
        'id': uuid.uuid4(), 
        'secret': 'secret1',
        'redirect_uri': 'https://github.com/michalswi/' 
    }
}

# my_services = {"services": [service1]}
my_services = {"services": [service1, service2]}

#-------------------
# API version check
def api_version_is_valid(api_version):
    version_data = api_version.split('.')
    result = True
    if (float(version_data[0]) < X_BROKER_API_MAJOR_VERSION or
       (float(version_data[0]) == X_BROKER_API_MAJOR_VERSION and
       float(version_data[1]) < X_BROKER_API_MINOR_VERSION)):
                result = False
    return result

def requires_api_version(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # check header
        api_version = request.headers.get('X-Broker-Api-Version')
        if (not api_version or not (api_version_is_valid(api_version))):
            abort(412)
        return f(*args, **kwargs)
    return decorated
 
@app.errorhandler(412)
def version_mismatch(error):
    return 'Version mismatch. Expected: {}: {}.{}'.format(
        X_BROKER_API_VERSION_NAME,
        X_BROKER_API_MAJOR_VERSION,
        X_BROKER_API_MINOR_VERSION), 412

#-------------------
# Authentication
def check_auth(username, password):
    if not (username == 'username' and password == 'password'):
        logger.info('Authentication failed')
    return username == 'username' and password == 'password'

def authenticate():
    return Response('You could not be verified.\n'
                    'Please login with the proper credentials.\n', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'}
                    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

#-------------------
# CATALOG
@app.route('/v2/catalog')
@requires_auth
@requires_api_version
def catalog():
    """
    Return the catalog of services handled by this broker
    """
    return jsonify(my_services)

# @app.route('/v2/service_instances/<instance_id>', methods=['PUT', 'DELETE','PATCH'])
# def service_instances(instance_id):
#     if request.method == 'PUT':
#         return make_response(jsonify({}), 201)
#     else:
#         return jsonify({})    

# ServiceInstance - provision + deprovision
@app.route('/v2/service_instances/<instance_id>', methods=['PUT', 'DELETE'])
@requires_auth
@requires_api_version
def service_instances(instance_id):
    """
    Provision an instance of this service and Deprovision an existing instance of this service
    <instance_id> is provided by Cloud Controller, used for future requests like bind, unbind and deprovision
    """

    # the payload format is in an unsupported format
    # if request.headers['Content-Type'] != 'application/json':
    #     abort(415, 'Unsupported Content-Type: expecting application/json')

    # do nothing just response
    if request.method == 'PUT':
        #1
        # return make_response(jsonify({}), 201)
        #2
        # TO DO: provision the service by calling out to the service itself
        new_service = {"dashboard_url": service_dashboard + instance_id}
        return jsonify(new_service)
    else:
        return jsonify({})

#ServiceBinding - bind + unbind
@app.route('/v2/service_instances/<instance_id>/service_bindings/<binding_id>', methods=['PUT', 'DELETE'])
@requires_auth
@requires_api_version
def service_binding(instance_id, binding_id):
    # <instance_id> is the Cloud Controller provided value used to provision the instance
    # <binding_id> is provided by the Cloud Controller  and will be used for future unbind requests

    # the payload format is in an unsupported format
    # if request.headers['Content-Type'] != 'application/json':
    #     abort(415, 'Unsupported Content-Type: expecting application/json')

    # do nothing just response
    if request.method == 'PUT':
        #1
        # TO DO: call the service here
        return make_response(jsonify({}), 201)
    else:
        return jsonify({})

#-------------------
# service endpoints related

#http://localhost:5000/sample-service/04a960ea-4c31-4d42-923b-df39117b1269
@app.route('/sample-service/<instance_id>', methods=['PUT','GET','DELETE'])
def provision_service(instance_id):
    service_info = {"get_instance_id": instance_id}
    return jsonify(service_info)

#http://localhost:5000/sample-service/dashboard/04a960ea-4c31-4d42-923b-df39117b1269
@app.route('/sample-service/dashboard/<instance_id>', methods=['GET'])
def dashboard(instance_id):
    # HTML, but could be a rendered template
    dashboard_page = render_template('base/dashboard.html')
    return dashboard_page

#http://localhost:5000/sample-service/04a960ea-4c31-4d42-923b-df39117b1269/test-service2-bkbb6-t8lph
@app.route('/sample-service/<instance_id>/<binding_id>', methods=['PUT','GET','DELETE'])
def bind_service(instance_id, binding_id):

    # if request.headers['Content-Type'] != 'application/json':
    #     abort(415, 'Unsupported Content-Type: expecting application/json')

    service_info = {"instance_id" : instance_id, "binding_id" : binding_id}
    return jsonify(service_info)

#-------------------

if __name__ == "__main__":
    # app.run(host = '0.0.0.0', port = int(service_port), debug = True)
    app.run(host = '0.0.0.0', port = int(service_port))