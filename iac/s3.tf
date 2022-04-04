resource "aws_s3_bucket" "pipe_bucket" {
  bucket = "age-predictions-tf-proba-pipe-artifacts"

  tags = {
    Name        = "age_prediction_tf_proba"
    Environment = "dev"
  }

}

resource "aws_s3_bucket_acl" "pipe_bucket_acl" {
  bucket = aws_s3_bucket.pipe_bucket.id
  acl    = "private"
}