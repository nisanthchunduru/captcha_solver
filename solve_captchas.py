import os
import re
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, utils
import cv2

import pdb

CAPTCHA_WIDTH = 120
CAPTCHA_HEIGHT = 80
CAPTCHA_TEXT_LENGTH = 6
TRAIN_DIRECTORY = 'data/captchas/train'
TEST_DIRECTORY = 'data/captchas/test'
CAPTCHA_FILENAME_PATTERN = r"\d+_([0-9]+)\.png"

from sklearn.preprocessing import OneHotEncoder
categories = [['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']]
ONE_HOT_ENCODER = OneHotEncoder(categories=categories)

def load_captcha_images(directory):
  filenames = []
  images = []
  encoded_texts = []
  for filename in os.listdir(directory):
    if not filename.endswith('.png'):
        continue

    image_path = os.path.join(directory, filename)
    image = read_captcha_image(image_path)

    match = re.match(CAPTCHA_FILENAME_PATTERN, filename)
    value = match.group(1)
    encoded_value = encode_captcha_text(value)

    filenames.append(filename)
    images.append(image)
    encoded_texts.append(encoded_value)

  return (filenames, images, encoded_texts)

def read_captcha_image(image_path):
  # image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
  # return image

  image = utils.load_img(image_path, color_mode='grayscale')
  image = np.array(image)
  image = image / 255.0
  image = np.expand_dims(image , axis=-1)
  return image

def normalize_image(image):
  return (image / 255.0)

# def convert_image_to_grayscale(image):
#   image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#   return image

def encode_captcha_text(value):
  return [encode_letter(c) for c in value]

def encode_letter(letter):
   return ONE_HOT_ENCODER.fit_transform([[letter]]).toarray()[0]

train_captchas_filenames, x_train, y_train = load_captcha_images(TRAIN_DIRECTORY)

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(CAPTCHA_HEIGHT, CAPTCHA_WIDTH, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(CAPTCHA_TEXT_LENGTH * 10, activation='softmax'))
model.add(layers.Reshape((CAPTCHA_TEXT_LENGTH, 10)))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# early_stopping = tf.keras.callbacks.EarlyStopping(monitor='accuracy', patience=3, mode='auto', min_delta=0.05)

model.fit(
    x=tf.stack(x_train),
    y=tf.stack(y_train),
    validation_split=0.2,
    epochs=100,
    # callbacks=[early_stopping]
)

def decode_prediction(prediction):
  value = ""
  for letter_prediction in prediction:
    letter = np.argmax(letter_prediction)
    value = value + str(letter)
  return value

test_captchas_filenames, x_test, y_test = load_captcha_images(TEST_DIRECTORY)
# model.predict(tf.stack([x_test[0]]))
predictions = model.predict(tf.stack(x_test))
decoded_predictions = [decode_prediction(prediction) for prediction in predictions]

pdb.set_trace()

