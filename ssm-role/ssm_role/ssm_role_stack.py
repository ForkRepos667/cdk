import json
from aws_cdk import (
    aws_iam as iam,
    core,
)


iam_role_properties={'':''}

class SsmRoleStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

    #################################################
    #
    # Create IAM role for ssm patching
    # 
    #################################################
            
            newRole = iam.Role(self, 'ssmCustomRole',
                            assumed_by=iam.ServicePrincipal("s3.amazonaws.com"),
                            role_name='ssmCustomRole'
                            )
            
            [newRole.add_to_policy(iam.PolicyStatement(resources=[key],actions=[value])) for key, value in iam_role_properties.items()]
        
        except:
            
            print('[-] Failed to execute AWS custome resource for S3 bucket')
            
 
