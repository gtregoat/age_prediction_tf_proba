ARG AWS_ACCOUNT_ID
ARG AWS_DEFAULT_REGION

FROM $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/age_prediction_tf_proba_container_repo:latest

ENV SAGEMAKER_PROGRAM model_logic.py