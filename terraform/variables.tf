variable "aws_region" {
  description = "AWS region for provisioning resources"
  type        = string
  default     = "ap-south-1"
}

variable "availability_zones" {
  description = "Explicit list of AWS Availability Zones (bypasses ec2:DescribeAvailabilityZones SCP restriction)"
  type        = list(string)
  default     = ["ap-south-1a", "ap-south-1b", "ap-south-1c"]
}

variable "project_name" {
  description = "Unique project identifier"
  type        = string
  default     = "podiumhq"
}

variable "environment" {
  description = "Target deployment environment"
  type        = string
  default     = "production"
}

variable "vpc_cidr" {
  description = "CIDR block for the AWS VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "cluster_version" {
  description = "Kubernetes control plane version"
  type        = string
  default     = "1.30"
}

variable "node_instance_types" {
  description = "EC2 instance types for EKS managed node group"
  type        = list(string)
  default     = ["t3.medium"]
}

variable "desired_nodes" {
  description = "Desired number of worker nodes"
  type        = number
  default     = 2
}

variable "min_nodes" {
  description = "Minimum number of worker nodes"
  type        = number
  default     = 2
}

variable "max_nodes" {
  description = "Maximum number of worker nodes"
  type        = number
  default     = 4
}
