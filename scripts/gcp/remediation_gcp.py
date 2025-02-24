# Remove Public Access from Google Cloud Storage Buckets

from google.cloud import storage

client = storage.Client()

def remediate_public_gcs(bucket_name):
    bucket = client.get_bucket(bucket_name)
    policy = bucket.get_iam_policy(requested_policy_version=3)
    bindings = [b for b in policy.bindings if 'allUsers' not in b['members']]
    policy.bindings = bindings
    bucket.set_iam_policy(policy)
    print(f"Public access removed from {bucket_name}.")

# Run the script for a sample GCS bucket
remediate_public_gcs("secure-gcs-bucket")
