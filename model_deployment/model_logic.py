import argparse
import os
import numpy as np
from age_model import TfProbabilityCnnClassifier
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sagemaker.amazon.amazon_estimator import RecordSet

# Note we cant use flow from directory with pipe as it requires tfrecords and no other
# than tf records can be streamed.


if __name__ == '__main__':
    print('initializing')
    parser = argparse.ArgumentParser()
    model = TfProbabilityCnnClassifier(input_dim=(128, 128, 3), n_classes=100)
    # params_dict = model.get_params()

    # Data, model, and output directories
    parser.add_argument('--output-data-dir', type=str, default=os.environ.get('SM_OUTPUT_DATA_DIR'))
    parser.add_argument('--model-dir', type=str, default=os.environ.get('SM_MODEL_DIR'))
    parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAIN'))
    parser.add_argument('--train-file', type=str)
    parser.add_argument('--test', type=str, default=os.environ.get('SM_CHANNEL_TEST'))
    parser.add_argument('--test-file', type=str, default=None)

    # Parameters
    parser.add_argument('--epochs', type=int, default=5)
    parser.add_argument('--steps_per_epoch', type=int, default=1000)
    parser.add_argument('--validation_steps', type=int, default=200)

    # for argument, default_value in model.items():
    #     parser.add_argument(f'--{argument}', type=type(default_value), default=default_value)

    print('reading arguments')
    args, _ = parser.parse_known_args()

    print(args)

    print('setting parameters')
    # gam_dict.update({key: value for key, value in vars(args).items() if key in gam_dict and value is not None})
    # gam.set_params(**gam_dict)

    print(model.summary())

    print('reading training data')
    # Train - Data Preparation - Data Augmentation with generators
    train_datagen = ImageDataGenerator(
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        brightness_range=[0.4, 1.5],
        rescale=1. / 255,
    )

    training_dataset = train_datagen.flow_from_directory(
        "data/train/",
        color_mode="rgb",
        batch_size=32,
        target_size=(128, 128),
        shuffle=True,
        seed=42,
        interpolation="bilinear",
        follow_links=False,
    )

    if args.test_file is not None:
        test_datagen = ImageDataGenerator(
            rescale=1. / 255,
        )

        test_dataset = test_datagen.flow_from_directory(
            "data/train/",
            color_mode="rgb",
            batch_size=32,
            target_size=(128, 128),
            shuffle=True,
            seed=42,
            interpolation="bilinear",
            follow_links=False,
        )
    else:
        test_dataset = None

    print('fitting model')
    model.fit(training_dataset, epochs=args.epochs,
              validation_data=test_dataset, steps_per_epoch=args.steps_per_epoch,
              validation_steps=args.validation_steps,
              )

    print(model.history.history)

    print('saving model')
    path = os.path.join(args.model_dir, "age_model")
    print(f"saving to {path}")
    model.save(path)


def model_fn(model_dir):
    return load_model(os.path.join(model_dir, "age_model"))


def predict_fn(input_object, m):
    return m.predict(input_object)
