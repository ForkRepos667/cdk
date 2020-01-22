from aws_cdk import (
    aws_ssm as ssm,
    aws_s3 as s3,
    aws_ec2 as ec2,
    core,
)


iam_role_properties={'':'',}


class ssmRoleStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


    #################################################
    #
    # Create IAM role for S3 bucket creation.
    # 
    #################################################
   
    try:

        newRole = iam.Role(self, 'ssmCustomRole',
                            assumed_by=iam.ServicePrincipal("ssm.amazonaws.com"),
                            role_name='ssmCustomRole'
                            )
       [newRole.add_to_policy(iam.PolicyStatement(resources=[key],actions=[value])) for key, value in iam_role_properties.items()]
        
   except:
            

    print('[-] Failed to execute AWS custome resource for S3 bucket')
