provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "my_bucket" {
  bucket = "multi-cloud-cspm-example"
  acl    = "private"

  tags = {
    Name = "MySecureS3Bucket"
  }
}
