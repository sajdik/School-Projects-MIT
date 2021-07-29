import tensorflow as tf
from tensorflow.keras.models import save_model, load_model
import matplotlib.pyplot as plt

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
train_dir = '../train'
val_dir = '../dev'
filepath = './saved_model'


nb_class = 31
batch_size = 8
epochs = 20

img_height = 80
img_width = 80

#Load data
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
  train_dir,
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
  val_dir,
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

whole_ds = train_ds.concatenate(val_ds)
whole_ds = whole_ds.shuffle(buffer_size=8)
train_ds = whole_ds.take(24)
val_ds = whole_ds.skip(24)

#Freeze top layers
model = load_model(filepath, compile = True)
model.layers[1].trainable = False
model.layers[2].trainable = False

#Training model
model.compile(
    loss= tf.losses.SparseCategoricalCrossentropy(from_logits=False),
    optimizer= tf.keras.optimizers.Adam(),
    metrics=['accuracy']
)

history = model.fit(
    train_ds,
    batch_size=batch_size,
    epochs=epochs,
    verbose=1,
    validation_data=val_ds
)

#Evaluate model
score = model.evaluate(val_ds, verbose=1)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# Save the model
filepath = './saved_model'
save_model(model, filepath)