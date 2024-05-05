import os
import re
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, utils
import cv2

CAPTCHA_WIDTH = 150
CAPTCHA_HEIGHT = 45
TRAIN_DIRECTORY = '/Users/nisanth/repos/andhra_pradesh_encumbrance_service_captcha_solver/data/captchas/train'
TEST_DIRECTORY = '/Users/nisanth/repos/andhra_pradesh_encumbrance_service_captcha_solver/data/captchas/test'
CAPTCHA_FILENAME_PATTERN = r"\d+_([0-9]+x*)\.jpg"

from sklearn.preprocessing import OneHotEncoder
categories = [['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'x']]
ONE_HOT_ENCODER = OneHotEncoder(categories=categories)

def load_captcha_images_and_values(directory):
  images = []
  encoded_values = []
  for filename in os.listdir(directory):
    if not filename.endswith('.jpg'):
        continue

    image_path = os.path.join(directory, filename)
    image = load_captcha_image(image_path)
    # import pdb; pdb.set_trace()
    # image = normalize_image(image)
    # image = np.expand_dims(image, axis=-1)
    # print(np.shape(image))
    images.append(image)

    match = re.match(CAPTCHA_FILENAME_PATTERN, filename)
    value = match.group(1)
    encoded_value = encode_value(value)
    # print(np.shape(encoded_value))
    encoded_values.append(encoded_value)
  
  return (images, encoded_values)

def load_captcha_image(image_path):
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

def encode_value(value):
  return [encode_letter(c) for c in value]
  # encoded_value = []
  # for letter in value:
  #   for number in encode_letter(letter):
  #     encoded_value.append(number)
  # return encoded_value

def encode_letter(letter):
   return ONE_HOT_ENCODER.fit_transform([[letter]]).toarray()[0]

x_train, y_train = load_captcha_images_and_values(TRAIN_DIRECTORY)

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(CAPTCHA_HEIGHT, CAPTCHA_WIDTH, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
# model.add(layers.Conv2D(16, (3, 3), activation='relu', input_shape=(CAPTCHA_HEIGHT, CAPTCHA_WIDTH, 1)))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Conv2D(32, (3, 3), activation='relu'))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(6 * 11, activation='softmax'))
model.add(layers.Reshape((6, 11)))
# model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(
    x=tf.stack(x_train),
    y=tf.stack(y_train),
    batch_size=1,
    epochs=100,
    validation_split=0.15
)

def decode_prediction(prediction):
  value = ""
  for letter_prediction in prediction:
    letter = np.argmax(letter_prediction)
    if not letter == 10:
      value = value + str(letter)
  return value

x_test, y_test = load_captcha_images_and_values(TEST_DIRECTORY)
# model.predict(tf.stack([x_test[0]]))
predictions = model.predict(tf.stack(x_test))

import pdb; pdb.set_trace()
