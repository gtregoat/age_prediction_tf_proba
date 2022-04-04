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

variable codestar_connector_credentials {
    type = string
}

variable branch_name {
  type = string
}