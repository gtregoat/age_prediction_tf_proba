# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.

from __future__ import print_function
from io import BytesIO
from flask import jsonify
import os
from age_model import TfProbabilityCnnClassifier
import numpy as np

import flask
from PIL import Image

prefix = "/opt/ml/"
model_path = os.path.join(prefix, "model")

# A singleton for holding the model. This simply loads the model and holds it.
# It has a predict function that does a prediction based on the model and the input data.


class ScoringService:
    """ToDo This is super weird lets change this when I know what is going on. Why class methods?"""
    model = None  # Where we keep the model when it's loaded

    @classmethod
    def get_model(cls):
        """Get the model object for this instance, loading it if it's not already loaded."""
        if cls.model is None:
            cls.model = TfProbabilityCnnClassifier(input_dim=(128, 128, 3), n_classes=100)
            cls.model.load_weights(os.path.join(model_path, "age_model"))
        return cls.model

    @classmethod
    def predict(cls, x):
        """For the input, do the predictions and return them.
        Args:
            x (a pandas dataframe): The data on which to do the predictions. There will be
                one prediction per row in the dataframe"""
        clf = cls.get_model()
        return clf.predict(x)


# The flask app for serving predictions
app = flask.Flask(__name__)


@app.route("/ping", methods=["GET"])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    health = ScoringService.get_model() is not None  # You can insert a health check here

    status = 200 if health else 404
    return flask.Response(response="\n", status=status, mimetype="application/json")


@app.route("/invocations", methods=["POST"])
def transformation():
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    # Read image
    if flask.request.content_type == "image/jpeg":
        data = flask.request.data
        data = np.array(Image.open(BytesIO(data)))
    else:
        return flask.Response(
            response="This predictor only supports jpg data", status=415, mimetype="text/plain"
        )
    # Do the prediction
    predictions = ScoringService.predict(data.reshape((1, 128, 128, 3)))
    return jsonify(predictions.tolist())
