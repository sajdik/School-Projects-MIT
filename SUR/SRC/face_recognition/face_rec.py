# Example of face detection with a vggface2 model
from keras.layers import Flatten, Dense, Dropout
from keras_vggface.vggface import VGGFace
import tensorflow as tf
from tensorflow.keras import layers, regularizers
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential, save_model

def plot_training_results():
  #Visualising training results
  #https://www.tensorflow.org/tutorials/images/classification#visualize_training_results_2

  acc = history.history['accuracy']
  val_acc = history.history['val_accuracy']

  loss = history.history['loss']
  val_loss = history.history['val_loss']

  epochs_range = range(epochs)

  plt.figure(figsize=(8, 8))
  plt.subplot(1, 2, 1)
  plt.plot(epochs_range, acc, label='Training Accuracy')
  plt.plot(epochs_range, val_acc, label='Validation Accuracy')
  plt.legend(loc='lower right')
  plt.title('Training and Validation Accuracy')

  plt.subplot(1, 2, 2)
  plt.plot(epochs_range, loss, label='Training Loss')
  plt.plot(epochs_range, val_loss, label='Validation Loss')
  plt.legend(loc='upper right')
  plt.title('Training and Validation Loss')
  plt.show()


#Params
nb_class = 31
batch_size = 8
epochs = 50

img_height = 80
img_width = 80

train_dir = '../train'
val_dir = '../dev'

#Loading data
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
  train_dir,
  labels='inferred',
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
  val_dir,
  labels='inferred',
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

#Setting up model
data_augmentation = Sequential(
  [
    layers.experimental.preprocessing.RandomFlip("horizontal", input_shape=(img_height, img_width, 3)),
    layers.experimental.preprocessing.RandomRotation(0.2),
    layers.experimental.preprocessing.RandomZoom(0.3),
    layers.experimental.preprocessing.RandomContrast(0.1),
  ]
)

vggFace = VGGFace(model='vgg16', include_top=False, input_shape=(img_height, img_width, 3))

# Freeze all the layers
for layer in vggFace.layers[:]:
    layer.trainable = False

custom_vgg_model = Sequential()
custom_vgg_model.add(layers.experimental.preprocessing.Rescaling(1./255))
custom_vgg_model.add(data_augmentation)
custom_vgg_model.add(vggFace)
custom_vgg_model.add(Dropout(0.25))
custom_vgg_model.add(Flatten(name='flatten'))
custom_vgg_model.add(Dense(1024, activation='relu', kernel_regularizer=regularizers.l2(0.001), name='fc6'))
custom_vgg_model.add(Dropout(0.5))
custom_vgg_model.add(Dense(512, activation='relu', kernel_regularizer=regularizers.l2(0.001), name='fc7'))
custom_vgg_model.add(Dropout(0.5))
custom_vgg_model.add(Dense(nb_class, activation='softmax', name='fc8'))

#Training model
custom_vgg_model.compile(
    loss= tf.losses.SparseCategoricalCrossentropy(from_logits=False),
    optimizer= tf.keras.optimizers.Nadam(),
    metrics=['accuracy']
)

history = custom_vgg_model.fit(
    train_ds,
    batch_size=batch_size,
    epochs=epochs,
    verbose=1,
    validation_data=val_ds
)

#Evaluate model
score = custom_vgg_model.evaluate(val_ds, verbose=1)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# Save the model
filepath = './saved_model'
save_model(custom_vgg_model, filepath)
