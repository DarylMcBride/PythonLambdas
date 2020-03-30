import json
import boto3
def lambda_handler(event, context):
    client = boto3.client('s3')
    enabled_list = []
    list_buckets = client.list_buckets()
    for bucket in list_buckets['Buckets']:
        bucket = bucket['Name']
        response = client.get_bucket_versioning(Bucket=bucket)
        if ('Status' in response and response['Status'] != 'Enabled') or 'Status' not in response:
            print(bucket)
            try:
                print(response['Status'])
            except:
                print('Not enabled')
            bucket_versioning = client.put_bucket_versioning(
                Bucket=bucket,
                VersioningConfiguration={
                    'Status': 'Enabled'
                }
            )
            enabled_list.append(bucket)
    print(len(enabled_list))
    return(enabled_list)