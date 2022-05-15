ARG AWS_ACCOUNT_ID
ARG AWS_DEFAULT_REGION

#FROM $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/age_prediction_tf_proba_container_repo:latest
#FROM 763104351884.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/tensorflow-training:2.8.0-gpu-py39-cu112-ubuntu20.04-sagemaker
FROM tensorflow/tensorflow:latest-gpu
ARG EXTRA_INDEX

ENV PATH="/opt/ml/code:${PATH}"
COPY . /opt/ml/code
RUN apt-key del F60F4B3D7FA2AF80
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
RUN apt-get -y update && apt-get install -y --no-install-recommends \
         nginx \
    && rm -rf /var/lib/apt/lists/*


RUN pip install age-model --extra-index-url $EXTRA_INDEX
WORKDIR /opt/ml/code
RUN pip install flask
RUN pip install gunicorn



ENV SAGEMAKER_PROGRAM model_logic.py