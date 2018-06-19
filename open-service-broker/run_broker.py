#!/usr/bin/env python

# https://pypi.org/project/openbrokerapi/
# http://openbrokerapi.readthedocs.io/en/latest/openbrokerapi.html

from flask import Flask
from openbrokerapi import api
from openbrokerapi.catalog import (ServicePlan,)
from openbrokerapi.log_util import basic_config
from openbrokerapi.service_broker import (
    ServiceBroker,
    Service,
    ProvisionedServiceSpec,
    UpdateServiceSpec,
    Binding,
    DeprovisionServiceSpec,
    LastOperation,
    UnbindDetails,
    ProvisionDetails,
    UpdateDetails,
    BindDetails,
    DeprovisionDetails
)

class ExampleServiceBroker(ServiceBroker):
    def catalog(self):
        return Service(
            id='00000000-0000-0000-0000-000000000000',
            name='example-service',
            description='Example Service does nothing',
            bindable=True,
            plans=[
                ServicePlan(
                    id='00000000-0000-0000-0000-000000000000',
                    name='small',
                    description='example service plan',
                ),
            ],
            tags=['example', 'service'],
            plan_updateable=True,
        )

    def provision(self, instance_id: str, service_details: ProvisionDetails,
                  async_allowed: bool) -> ProvisionedServiceSpec:
        pass

    def unbind(self, instance_id: str, binding_id: str, details: UnbindDetails):
        pass

    def update(self, instance_id: str, details: UpdateDetails, async_allowed: bool) -> UpdateServiceSpec:
        pass

    def bind(self, instance_id: str, binding_id: str, details: BindDetails) -> Binding:
        pass

    def deprovision(self, instance_id: str, details: DeprovisionDetails, async_allowed: bool) -> DeprovisionServiceSpec:
        pass

    def last_operation(self, instance_id: str, operation_data: str) -> LastOperation:
        pass


# Simply start the server
# api.serve(ExampleServiceBroker(), api.BrokerCredentials("", ""))

# or start the server without authentication
# api.serve(ExampleServiceBroker(), None)

# or with multiple service brokers
# api.serve([ExampleServiceBroker(), ExampleServiceBroker()], api.BrokerCredentials("", ""))

# or register blueprint to your own FlaskApp instance
app = Flask(__name__)
# Use root logger with a basic configuration provided by openbrokerapi.log_utils
logger = basic_config()  
openbroker_bp = api.get_blueprint(ExampleServiceBroker(), api.BrokerCredentials(username="username", password="password"), logger)
# openbroker_bp = api.get_blueprint(ExampleServiceBroker(), api.BrokerCredentials("username", "password"), logger)
# if more than one service:
# openbroker_bp = api.get_blueprint([ExampleServiceBroker(),...], api.BrokerCredentials(username="user", password="pass"), logger)

app.register_blueprint(openbroker_bp)

# default port 5000 is exposed
app.run("0.0.0.0", debug=True)
# if __name__ == "__main__":
#     app.run("0.0.0.0", 5000, True)

