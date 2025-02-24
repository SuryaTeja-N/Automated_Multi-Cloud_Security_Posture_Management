package security

deny[msg] if {
    input.bucket_public == true
    msg := "Public S3 buckets are not allowed!"
}

# to test, run :

# echo '{"bucket_public": true}' > input.json && opa eval --input input.json --data policy.rego --format pretty "data.security.deny"




