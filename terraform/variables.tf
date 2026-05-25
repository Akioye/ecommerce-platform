variable "aws_region" {
  description = "AWS region to deploy resources"
  default     = "us-east-1"
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  default     = "ecommerce-cluster"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}