#!/usr/bin/env python3

from aws_cdk import core


from patching.patching_stack import PatchingStack
from patching.patching_endpoint_stack import PatchingEndpointStack
from patching.patching_new_endpoint_stack import NewPatchingEndpointStack


app = core.App()

# Stacks
endpointStack = PatchingEndpointStack(app, "endpoint", env={ 'region': "eu-west-2", 'account': "847208056990"})
newendpointStack = NewPatchingEndpointStack(app, "newendpoint", env={ 'region': "eu-west-2", 'account': "847208056990"})
patchingStack = PatchingStack(app, "patching", env={ 'region': "eu-west-2", 'account': "847208056990"})


app.synth()