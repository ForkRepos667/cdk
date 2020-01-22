from aws_cdk import (
    aws_ssm as ssm,
    aws_s3 as s3,
    aws_ec2 as ec2,
    core,
)


class ssmRoleStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        ec2_endpoint = ec2.VpcEndpoint(self, 
                                        id="ssm-endpoint",
                                        VpcEndpointType='Interface',
                                        VpcId='string',
                                        ServiceName='string',
                                        PolicyDocument='string',
                                        RouteTableIds=['string',],
                                        SubnetIds=['string',],
                                        SecurityGroupIds=['string',],
                                        ClientToken='string',
                                        PrivateDnsEnabled=True
                                        )
                                       
    
