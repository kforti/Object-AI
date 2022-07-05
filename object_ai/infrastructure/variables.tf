variable "region" {
  type        = string
  description = "aws region to deploy into"
  default     = "us-east-1"
}

//variable "aws_account_id" {
//  description = "aws_account_id"
//  type        = string
//}

variable "aws_profile" {
  description = "aws profile to use for credentials"
  type = string
  default = "default"
}

variable "s3_bucket_name" {
  description = "name of the user's bucket where datasets will be saved"
  type = string
}