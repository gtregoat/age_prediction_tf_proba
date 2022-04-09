resource "aws_ecr_repository" "age_prediction_tf_proba_container_repo" {
  name                 = "age_prediction_tf_proba_container_repo"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
