import boto3

def remediate_public_s3(bucket_name):
    s3 = boto3.client('s3')

    # Get bucket ACL
    acl = s3.get_bucket_acl(Bucket=bucket_name)
    for grant in acl['Grants']:
        if "AllUsers" in grant["Grantee"].get("URI", ""):
            print(f"Public access found! Remediating {bucket_name}...")
            s3.put_bucket_acl(Bucket=bucket_name, ACL="private")
            print(f"Remediated: {bucket_name} is now private.")

def lambda_handler(event, context):
    # Extract bucket name from the event
    bucket_name = event['detail']['requestParameters']['bucketName']
    print(f"Trigger received for bucket: {bucket_name}")
    
    remediate_public_s3(bucket_name)
    
    return {
        'statusCode': 200,
        'body': f"Remediated public bucket: {bucket_name}"
    }
