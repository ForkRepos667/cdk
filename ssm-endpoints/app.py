#!/usr/bin/env python3

from aws_cdk import core

from ssm_endpoints.ssm_endpoints_stack import SsmEndpointsStack


app = core.App()
SsmEndpointsStack(app, "ssm-endpoints")

app.synth()
