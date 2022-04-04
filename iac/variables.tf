variable "terraform_docker" {
  type = string
}

variable "code_pipeline_version" {
  type = string
}

variable "codestar_version" {
  type = string
}

variable "github_repo" {
  type = string
}

variable branch_name {
  type = string
}

data "aws_secretsmanager_secret_version" "codestar_creds" {
  # Fill in the name you gave to your secret
  secret_id = "age_pred_tf_proba_codestar_arn"
}

locals {
  codestar_connector_credentials = jsondecode(
    data.aws_secretsmanager_secret_version.codestar_creds.secret_string
  )
}