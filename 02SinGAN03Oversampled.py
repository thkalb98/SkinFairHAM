exp_name="02SinGAN03Oversampled" # from the series of SinGAN augmented, where the dataset is actually augmented.
batch_size=16
lr=1e-5
ita_threshold=41
seed = 2307

import tensorflow as tf
from utils import visualize_history,run_experiment,save_predictions
print("Succesfully imported all libraries")
print(tf.__version__)
from tensorflow.python.client import device_lib
device_lib.list_local_devices()
import pathlib
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from utils import create_dataset,prepare_df,parse_function, recalculate_weights

TRAINING_PATH = "./data/ISIC2018/ISIC2018_Task3_Training_Input/"

df_train_temp = prepare_df(TRAINING_PATH).dropna()
forbidden_images = ["ISIC_0024962.jpg","ISIC_0025927.jpg","ISIC_0032149.jpg"]
for fi in forbidden_images: # they still need to be removed from the training
    df_train_temp = df_train_temp.drop(df_train_temp[df_train_temp['image'] == fi].index)

print("{} samples are used".format(len(df_train_temp)))

df_train=df_train_temp[df_train_temp["estimated_ita"]>ita_threshold]
df_test = df_train_temp[df_train_temp["estimated_ita"]<=ita_threshold]

from sklearn.model_selection import train_test_split
idx_train, idx_valid = train_test_split(df_train.index,stratify=df_train["lesion"],test_size=0.20,random_state=seed,shuffle=True)

df_valid = df_train.loc[idx_valid,:]
df_train = df_train.loc[idx_train,:]

print("number of training samples before oversampling: {}".format(len(df_train)))
df_oversampling = pd.DataFrame(data={"image":forbidden_images,"lesion":["MEL","MEL","MEL"]})
row_idx_repeated = np.repeat(df_oversampling.index,100) # create three-hundred images
df_oversampling = df_oversampling.iloc[row_idx_repeated,:]
df_train = pd.concat((df_train,df_oversampling),ignore_index=True)
print("number of training samples after oversampling: {}".format(len(df_train)))

# re-calculate weights
df_train = recalculate_weights(df_train)
df_valid = recalculate_weights(df_valid)
df_test = recalculate_weights(df_test)

train_data = create_dataset(df_train,TRAINING_PATH,shuffle=True).batch(batch_size)
valid_data = create_dataset(df_valid,TRAINING_PATH).batch(batch_size)

test_data = create_dataset(df_test,TRAINING_PATH).batch(batch_size)

print("Datasets succsefully created and edited")

model = tf.keras.applications.MobileNetV2(
    input_shape=None,
    alpha=1.0,
    include_top=True,
    weights="imagenet",
    input_tensor=None,
    pooling="avg",
    classes=1000,
    classifier_activation="softmax",
)

# adapt the model
last_layer = model.layers[-2].output

output = tf.keras.layers.Dense(7, activation='softmax', name='predict_class')(last_layer)
# building and printing the final model
model = tf.keras.models.Model(inputs=model.layers[0].output,outputs=output)

opt = tf.keras.optimizers.Adam(learning_rate=lr)
model.compile(loss='sparse_categorical_crossentropy',
              optimizer=opt,
              weighted_metrics=[tf.keras.metrics.SparseCategoricalAccuracy()])

print("Model created and compiled. Start training now")

run_experiment(model,train_data,valid_data,exp_name=exp_name,patience=30,epochs=90)

print("Trainnig completed. Saving predictions now.")
save_predictions(exp_name,df_test,data_path = TRAINING_PATH)