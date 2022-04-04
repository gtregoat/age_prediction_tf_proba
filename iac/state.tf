terraform{
  backend "s3" {
    bucket = "tregoat-ci-cd"
    encrypt = true
    key = "terraform.tfstate"
    region = "eu-west-1"
  }
}