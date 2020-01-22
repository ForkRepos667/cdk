import cfnresponse

def handler(event, context):
        print(event)
                        
        # Globals
        responseData = {}
        ResponseStatus = cfnresponse.SUCCESS
                        
        s3bucketName = event['ResourceProperties']['s3bucketName']
                        
        if event['RequestType'] == 'Create':
            pass
                        
        elif event['RequestType'] == 'Update':
                            
            pass
                        
        elif event['RequestType'] == 'Delete':
                            
            # Need to empty the S3 bucket before it is deleted
            s3 = boto3.resource('s3')
            
            s3bucketName = event['ResourceProperties']['BucketName]
                           
            bucket = s3.Bucket(s3bucketName)
            bucket.objects.all().delete()
            
        
        cfnresponse.send(event, context, ResponseStatus, responseData)