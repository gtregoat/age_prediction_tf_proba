resource "aws_codebuild_project" "tf-plan" {
  name          = "tf-cicd-plan"
  description   = "Plan stage for terraform"
  service_role  = aws_iam_role.tf-codebuild-role.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = var.terraform_docker
    type                        = "LINUX_CONTAINER"
    image_pull_credentials_type = "SERVICE_ROLE"
#    registry_credential{
#        credential = var.dockerhub_credentials
#        credential_provider = "SECRETS_MANAGER"
#    }
 }
 source {
     type   = "CODEPIPELINE"
     buildspec = file("../buildspec/plan-buildspec.yaml")
 }
}

resource "aws_codebuild_project" "tf-apply" {
  name          = "tf-cicd-apply"
  description   = "Apply stage for terraform"
  service_role  = aws_iam_role.tf-codebuild-role.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = var.terraform_docker
    type                        = "LINUX_CONTAINER"
    image_pull_credentials_type = "SERVICE_ROLE"
#    registry_credential{
#        credential = var.dockerhub_credentials
#        credential_provider = "SECRETS_MANAGER"
#    }
 }
 source {
     type   = "CODEPIPELINE"
     buildspec = file("../buildspec/apply-buildspec.yaml")
 }
}


resource "aws_codepipeline" "cicd_pipeline" {

    name = "tf-cicd"
    role_arn = aws_iam_role.age_prediction_tf_proba_codepipeline_role.arn

    artifact_store {
        type="S3"
        location = aws_s3_bucket.pipe_bucket.id
    }

    stage {
        name = "Source"
        action{
            name = "Source"
            category = "Source"
            owner = "AWS"
            provider = "CodeStarSourceConnection"
            version = var.codestar_version
            output_artifacts = ["tf-code"]
            configuration = {
                FullRepositoryId = var.github_repo
                BranchName   = var.branch_name
                ConnectionArn = local.codestar_connector_credentials.age_pred_tf_proba_codestar_arn
                OutputArtifactFormat = "CODE_ZIP"
            }
        }
    }

    stage {
        name ="Plan"
        action{
            name = "Build"
            category = "Build"
            provider = "CodeBuild"
            version = var.code_pipeline_version
            owner = "AWS"
            input_artifacts = ["tf-code"]
            configuration = {
                ProjectName = "tf-cicd-plan"
            }
        }
    }

    stage {
        name ="Deploy"
        action{
            name = "Deploy"
            category = "Build"
            provider = "CodeBuild"
            version = var.code_pipeline_version
            owner = "AWS"
            input_artifacts = ["tf-code"]
            configuration = {
                ProjectName = "tf-cicd-apply"
            }
        }
    }

}