########################################################
#
# Lambda function creates/deletes S3 bucket and contents
# v0.1 
# Phil H
#
########################################################

import boto3
import json
import logging
import urllib3


# Logger settings - CloudWatch
# Set level to DEBUG for debugging, INFO for general usage.
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    
    # Get properties
    location = event['ResourceProperties']['loc']
    bucket = event['ResourceProperties']['bktname']
    
    logger.info("Received property: " + bucket)
    logger.info("Received property: " + location)
    
    s3_client = boto3.resource('s3')
    
    logger.info("Received event: " + json.dumps(event, indent=2))

    try:
        if event["RequestType"] == "Create":

            s3_client.create_bucket(Bucket=bucket,
                                    CreateBucketConfiguration={'LocationConstraint': location}
                                   )
                                   
            responseStatus = 'SUCCESS'                                   

        elif event["RequestType"] == "Delete":

            s3_client.Bucket(bucket).objects.all().delete()
            s3_client.Bucket(bucket).delete()
            
            #Required for S3 versioning
            #bucket.object_versions.delete()

            responseStatus = 'SUCCESS'

    except Exception as e:
        logger.error( "An error occured: {}".format(e) )

        responseStatus = 'FAILURE'
    
    # Send response to CloudFormation to notify that resource creation is successful/failed
    send_response(responseStatus, event, context)


def send_response(responseStatus, event, context):
   
   
    request_body = {
        "Status": responseStatus,
        "StackId" : event["StackId"],
        'PhysicalResourceId': context.log_stream_name,
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
    }
    logger.debug(request_body)
    
    try:
        reqs = urllib3.PoolManager()
        
        enc_data = json.dumps(request_body).encode('utf-8')
    
        response = reqs.request('PUT', event['ResponseURL'], body=enc_data)
        
        if response.status != 200:
             logger.info("Error status: " + reqs.status)
            
        return
    
    except Exception as e:
        logger.error( "An error occured: {}".format(e) )