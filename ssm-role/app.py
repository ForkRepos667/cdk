#!/usr/bin/env python3

from aws_cdk import core

from ssm_role.ssm_role_stack import SsmRoleStack


app = core.App()
SsmRoleStack(app, "ssm-role")

app.synth()
