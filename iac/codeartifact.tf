resource "aws_kms_key" "age_prediction_tf_proba_kms" {
  description = "age_prediction_tf_proba domain key"
}


resource "aws_codeartifact_domain" "age_prediction_tf_proba_domain" {
  domain         = "tregoat-packages"
  encryption_key = aws_kms_key.age_prediction_tf_proba_kms.arn
}


resource "aws_codeartifact_repository" "age-distribution" {
  repository = "age-distribution"
  domain     = aws_codeartifact_domain.age_prediction_tf_proba_domain.domain
}


# To allow access to the CodeArtifact repository without going through the internet,
# we will need a VPC endpoint that accepts traffic from the previously created subnet
resource "aws_security_group" "age_prediction_tf_proba_codeartifact" {
  name        = "age_prediction_tf_proba-SecurityGroup"
  vpc_id      = aws_vpc.age_prediction_tf_proba_vpc.id

  ingress {
    description = "TLS from Subnet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [aws_subnet.age_prediction_tf_proba_subnet.cidr_block]
  }

  tags = {
    age_prediction_tf_proba = "Code Artifact Security Group"
  }
}


# Set up a VPC to we can deactivate downloading through the internet.
# To download the packages, we'll have to set the machine to be on the
# VPC.
# Therefore, we create that VPC and we create an IAM policy that restricts
# Access to that code artifact repository to machines on the VPC.

data "aws_vpc_endpoint_service" "codeartifact" {
  service = "codeartifact.api"
}


resource "aws_vpc_endpoint" "age_prediction_tf_proba_codeartifact" {
  vpc_id            = aws_vpc.age_prediction_tf_proba_vpc.id
  service_name      = data.aws_vpc_endpoint_service.codeartifact.service_name
  vpc_endpoint_type = "Interface"

  security_group_ids = [
    aws_security_group.age_prediction_tf_proba_codeartifact.id,
  ]

  private_dns_enabled = true

  tags = {
    age_prediction_tf_proba = "Codeartifact-Endpoint"
  }
}