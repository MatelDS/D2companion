# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from keras.models import Model
from keras.layers import Input, Dense, Flatten, Reshape

from skimage.metrics import structural_similarity as ssim

from mlutils import d2DataSet

##Hyperparameter##
DATA_PATH = "C:\\PyCode\\Projects\\D2companion\\data"

scale_factor = 4
IMAGE_SIZE = (int(646/scale_factor), int(509/scale_factor))
ENCODING_DIM = 1024

EPOCHS = 2
BATCH_SIZE = 16

##load images##
dataset = d2DataSet()
dataset.set_path(DATA_PATH)
dataset.find_images()
#dataset.filter_imgs("Amazon")

data = dataset.get_data(load_imgs=True, img_size=IMAGE_SIZE, greyscale=True, img_mode="numpy")
imgs = np.stack(data["img"])/255.0
y = data[["mouse","mouse_x", "mouse_y", "keyboard"]]

##autoencoder model definition##
INPUT_SHAPE = imgs[0].shape
input_img = Input(shape=INPUT_SHAPE)

encoded = Flatten()(input_img)
encoded = Dense(ENCODING_DIM, activation="relu")(encoded)
decoded = Dense(np.prod(INPUT_SHAPE), activation="sigmoid")(encoded)
decoded = Reshape(INPUT_SHAPE)(decoded)

autoencoder = Model(input_img, decoded)
encoder = Model(input_img, encoded)

decoder_input = Input(shape=(ENCODING_DIM,))
deco = autoencoder.layers[-2](decoder_input)
deco = autoencoder.layers[-1](deco)

decoder = Model(decoder_input, deco)

autoencoder.compile(loss='mse', optimizer='adam')
decoder.compile(loss='mse', optimizer='adam')

#train autoencoder
autoencoder.fit(imgs,
                imgs,
                epochs=EPOCHS,
                batch_size=BATCH_SIZE)

preds = autoencoder.predict(imgs)

img_ssim = [ssim(imgs[i], preds[i], multichannel=True) for i in range(len(imgs))]
