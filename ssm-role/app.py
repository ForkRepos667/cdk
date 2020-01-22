#!/usr/bin/env python3

from aws_cdk import core

from ssm_role.ssm_role_stack import ssmRoleStack


app = core.App()
ssmRoleStack(app, "ssm-role")

app.synth()
