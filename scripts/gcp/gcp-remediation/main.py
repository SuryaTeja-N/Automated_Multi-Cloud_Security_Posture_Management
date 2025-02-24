import os
from google.cloud import storage

# Set authentication credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp-key.json"

storage_client = storage.Client()

def remediate_public_gcs(event, context):
    bucket_name = event['bucket']
    print(f"Checking security settings for bucket: {bucket_name}")

    bucket = storage_client.bucket(bucket_name)
    policy = bucket.get_iam_policy()

    # Remove public access if found
    filtered_bindings = [b for b in policy.bindings if "allUsers" not in b['members']]
    if len(filtered_bindings) != len(policy.bindings):
        policy.bindings = filtered_bindings
        bucket.set_iam_policy(policy)
        print(f"✅ Public access removed from {bucket_name}")
    else:
        print(f"🔒 {bucket_name} is already secure.")
