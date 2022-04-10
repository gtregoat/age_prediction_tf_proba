# The following VPCs are to restrict access to code artifact
# to machines that are on these VPCs
resource "aws_vpc" "age_prediction_tf_proba_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    age_prediction_tf_proba = "VPC",
    description = "Useful for code artifact"
  }
}

resource "aws_subnet" "age_prediction_tf_proba_subnet" {
  vpc_id     = aws_vpc.age_prediction_tf_proba_vpc.id
  cidr_block = "10.0.1.0/24"

  tags = {
    age_prediction_tf_proba = "subnet",
    description = "Useful for code artifact"
  }
}