terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}

provider "aws" {
  region  = var.region
  shared_credentials_files = ["${pathexpand("~/.aws/credentials")}"]
  profile                 = var.aws_profile

}

resource "aws_s3_bucket" "b" {
  bucket = "my-tf-test-bucket"

}

resource "aws_s3_bucket_acl" "example" {
  bucket = aws_s3_bucket.b.id
  acl    = "private"
}