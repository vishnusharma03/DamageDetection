# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.

from __future__ import print_function
from ultralytics import YOLO
import io
import json
import os
import flask
import traceback
import logging
import sys
from PIL import Image

prefix = "/opt/ml/"
model_path = os.path.join(prefix, "model")
param_path = os.path.join(prefix, 'input/config/hyperparameters.json')
output_path = os.path.join(prefix, 'output')

with open(param_path, 'r') as tc:
    trainingParams = json.load(tc)

imgsiz = trainingParams.get('imgsize', 614)


# A singleton for holding the model. This simply loads the model and holds it.
# It has a predict function that does a prediction based on the model and the input data.


class Prediction(object):
    model = None  # Where we keep the model when it's loaded

    @classmethod
    def get_model(cls):
        """Get the model object for this instance, loading it if it's not already loaded."""
        if cls.model is None:
            cls.model = YOLO(os.path.join(model_path, "train", "weights", "best.pt"))
        return cls.model

    @classmethod
    def predict(cls, inputx):
        """For the input, do the predictions and return them.

        Args:
            inputx (a pandas dataframe): The data on which to do the predictions. There will be
                one prediction per row in the dataframe"""
        argsone = {"source": inputx, "save": True}
        clf = cls.get_model()
        return clf.predict(**argsone)


# The flask app for serving predictions
app = flask.Flask(__name__)


@app.route("/ping", methods=["GET"])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    health = Prediction.get_model() is not None  # You can insert a health check here

    status = 200 if health else 404
    return flask.Response(response="\n", status=status, mimetype="application/json")


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}


def allowed_file(filename):
    """Checks if the filename extension is allowed."""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_image(img):
    try:
        new_size = (imgsiz, imgsiz)
        img = Image.open(img.stream)
        resized_img = img.resize(new_size)
        return resized_img

    except Exception as e:
        # Write out an error file. This will be returned as the failureReason in the
        # DescribeTrainingJob result.
        trc = traceback.format_exc()
        with open(os.path.join(output_path, 'failure'), 'w') as s:
            s.write('Exception during training: ' + str(e) + '\n' + trc)
        # Printing this causes the exception to be in the training job logs, as well.
        print('Exception during training: ' + str(e) + '\n' + trc, file=sys.stderr)
        # A non-zero exit code causes the training job to be marked as Failed.
        sys.exit(255)


@app.route("/invocations", methods=["POST"])
def transformation():
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.)
    """
    try:
        pImg = None

        if flask.request.method == 'POST':
            if 'image' not in flask.request.files:
                return flask.Response(
                    response="Missing image file", status=400, mimetype="text/plain"
                )
            file = flask.request.files['image']
            ext = file.filename.rsplit('.', 1)[1].lower()
            if file.filename == '':
                return flask.Response(
                    response="No selected file", status=400, mimetype="text/plain"
                )

            if file and allowed_file(file.filename):
                pImg = process_image(file)

            else:
                return flask.Response(
                    response="Unsupported file format. Only jpg, jpeg, and png allowed.",
                    status=415,
                    mimetype="text/plain"
                )

        print("Invoked Successfully.")
        logging.log(1, "Invocation Successful")

        # Do the prediction
        predictions = Prediction.predict(pImg)

        img_io = io.BytesIO()
        for num, pre in enumerate(predictions):
            pre.save(filename="result"+str(num) + "." + ext)
            # pre.save(img_io, format='JPEG' if pre.format == 'JPEG' else 'PNG')  # Convert to JPEG or PNG
            img_io.seek(0)

        return flask.send_file(img_io, mimetype='image/jpeg' if pImg.format == 'JPEG' else 'image/png')

    except Exception as e:
        # Write out an error file. This will be returned as the failureReason in the
        # DescribeTrainingJob result.
        trc = traceback.format_exc()
        with open(os.path.join(output_path, 'failure'), 'w') as s:
            s.write('Exception during training: ' + str(e) + '\n' + trc)
        # Printing this causes the exception to be in the training job logs, as well.
        print('Exception during training: ' + str(e) + '\n' + trc, file=sys.stderr)
        # A non-zero exit code causes the training job to be marked as Failed.
        sys.exit(255)

