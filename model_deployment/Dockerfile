ARG AWS_ACCOUNT_ID
ARG AWS_DEFAULT_REGION

FROM $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/age_prediction_tf_proba_container_repo:latest

ENV PATH="/opt/ml/code:${PATH}"
COPY . /opt/ml/code

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         nginx \
    && rm -rf /var/lib/apt/lists/*



WORKDIR /opt/ml/code
RUN pip install flask
RUN pip install gunicorn

ENV SAGEMAKER_PROGRAM model_logic.py