resource "aws_iam_role" "age_prediction_tf_proba_codepipeline_role" {
  name = "age_prediction_tf_proba_codepipeline_role"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Sid       = ""
        Principal = {
          Service = "codepipeline.amazonaws.com"
        }
      },
    ]
  })
}


data "aws_iam_policy_document" "tf-cicd-pipeline-policies" {
  statement {
    sid       = ""
    actions   = ["codestar-connections:UseConnection"]
    resources = ["*"]
    effect    = "Allow"
  }
  statement {
    sid       = ""
    actions   = ["cloudwatch:*", "s3:*", "codebuild:*"]
    resources = ["*"]
    effect    = "Allow"
  }
}

resource "aws_iam_policy" "tf-cicd-pipeline-policy" {
  name        = "tf-cicd-pipeline-policy"
  path        = "/"
  description = "Pipeline policy"
  policy      = data.aws_iam_policy_document.tf-cicd-pipeline-policies.json
}

resource "aws_iam_role_policy_attachment" "tf-cicd-pipeline-attachment" {
  policy_arn = aws_iam_policy.tf-cicd-pipeline-policy.arn
  role       = aws_iam_role.age_prediction_tf_proba_codepipeline_role.id
}


resource "aws_iam_role" "tf-codebuild-role" {
  name = "tf-codebuild-role"

  assume_role_policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Action" : "sts:AssumeRole",
          "Principal" : {
            "Service" : "codebuild.amazonaws.com"
          },
          "Effect" : "Allow",
          "Sid" : ""
        }
      ]
    })
}

data "aws_iam_policy_document" "tf-cicd-build-policies" {
  statement {
    sid       = ""
    actions   = ["logs:*", "s3:*", "codebuild:*", "secretsmanager:*", "iam:*"]
    resources = ["*"]
    effect    = "Allow"
  }
}

resource "aws_iam_policy" "tf-cicd-build-policy" {
  name        = "tf-cicd-build-policy"
  path        = "/"
  description = "Codebuild policy"
  policy      = data.aws_iam_policy_document.tf-cicd-build-policies.json
}

resource "aws_iam_role_policy_attachment" "tf-cicd-codebuild-attachment1" {
  policy_arn = aws_iam_policy.tf-cicd-build-policy.arn
  role       = aws_iam_role.tf-codebuild-role.id
}

resource "aws_iam_role_policy_attachment" "tf-cicd-codebuild-attachment2" {
  policy_arn = "arn:aws:iam::aws:policy/PowerUserAccess"
  role       = aws_iam_role.tf-codebuild-role.id
}


resource "aws_codeartifact_repository_permissions_policy" "age_prediction_tf_proba_code_artifact_iam" {
  repository      = aws_codeartifact_repository.age-distribution.repository
  domain          = aws_codeartifact_domain.age_prediction_tf_proba_domain.domain
  policy_document = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Action" : "codeartifact:Get*",
          "Effect" : "Allow",
          "Principal" : "*",
          "Resource" : "${aws_codeartifact_domain.age_prediction_tf_proba_domain.arn}"
          "Condition" : {
            "StringNotEquals" : {
              "aws:SourceVpce" : "${aws_vpc_endpoint.age_prediction_tf_proba_codeartifact.id}"
            }
          }
        }
      ]
    })
}

# Defining the SageMaker "Assume Role" policy
data "aws_iam_policy_document" "age_prediction_tf_proba_sagemaker_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type = "Service"
      identifiers = ["sagemaker.amazonaws.com"]
    }
  }
}



## RESOURCE BLOCKS
## ----------------------------------------------------------------

# Defining the SageMaker notebook IAM role
resource "aws_iam_role" "sagemaker_notebook_iam_role" {
  name = "sagemaker_notebook_iam_role"
  assume_role_policy = data.aws_iam_policy_document.age_prediction_tf_proba_sagemaker_assume_role_policy.json
}

# Attaching the AWS default policy, "AmazonSageMakerFullAccess"
resource "aws_iam_policy_attachment" "sagemaker_full_access" {
  name = "sm-full-access-attachment"
  roles = [aws_iam_role.sagemaker_notebook_iam_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}