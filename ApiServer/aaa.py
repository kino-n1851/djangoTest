import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
"""
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)

model.evaluate(x_test,  y_test, verbose=2)

s = model.predict_classes( x_test[:5] )
print(s)
a = y_test[:5]
print(a) 
print(a==s)
target = x_test[0]
s = model.predict_classes( target.reshape([1,28,28]) )
print(s[0])
model.save("saved_model/model_a")
"""
im = np.array(ImageOps.invert(Image.open('test6.png').convert('L')))
new_model = tf.keras.models.load_model('saved_model/model_a')
new_model.summary()
s = new_model.predict_classes( im.reshape([1,28,28]) )
print(s)