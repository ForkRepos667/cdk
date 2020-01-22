import json
from aws_cdk import (
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_s3 as s3,
    core,
)


#s3_Properties

bucket_properties={'bktname':'philbucket2', 'loc':'eu-west-2'}
iam_role_properties={'':'',}

class S3Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        """

            
        #################################################
        #
        # Create/Delete S3 bucket. (This will get called 
        # on CF create and delete event)
        # 
        #################################################

        try:

            
            s3_custom = cfn.CfnCustomResource(self, 
                                        's3_custom',
                                        service_token='arn:aws:lambda:eu-west-2:847208056990:function:s3_custom_function',
                                        )
            
            # Add propertie(s)
            
            [s3_custom.add_property_override(key, value)  for key, value in bucket_properties.items()]
                
        except:
            
            print('[-] Failed to execute AWS custome resource for S3 bucket')
            

  
  