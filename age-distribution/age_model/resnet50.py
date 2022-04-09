"""
Regular Resnet50
"""

# from tensorflow.keras.applications.resnet50 import ResNet50
# from tensorflow.keras.layers import Dropout, Flatten, Dense, GlobalAveragePooling2D
# import tensorflow as tf
#
#
# class ResNet50Classifier:
#     def __init__(self, input_shape):
#         model_pretrained = ResNet50(include_top=False, weights="imagenet",
#                                     input_shape=input_shape)
#         # Adding custom Layers
#         x = model_pretrained.output
#         x = GlobalAveragePooling2D()(x)
#         x = Dense(28, activation="relu")(x)
#         x = Dropout(0.3)(x)
#         x = Dense(56, activation="relu")(x)
#         predictions = Dense(100, activation="softmax")(x)
#         model = tf.keras.models.Model(inputs=model_pretrained.input, outputs=predictions)
#
#         model.compile(optimizer=tf.keras.optimizers.Adam(),
#                       loss="categorical_crossentropy",
#                       metrics=["accuracy", mae_as_reg, actual_accuracy])
