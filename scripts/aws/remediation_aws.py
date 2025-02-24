import boto3
# AWS: Remediate Public S3 Buckets

s3 = boto3.client("s3")

def remediate_public_s3(bucket_name):
    acl = s3.get_bucket_acl(Bucket=bucket_name)
    for grant in acl["Grants"]:
        if "AllUsers" in grant["Grantee"].get("URI", ""):
            print(f"Public access found! Remediating {bucket_name}...")
            s3.put_bucket_acl(Bucket=bucket_name, ACL="private")
            print(f"Remediated: {bucket_name} is now private.")

# Run the script for a sample bucket
remediate_public_s3("suryabucket143")
