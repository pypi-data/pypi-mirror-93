
# EasyDL
EasyDL - Where Deep learning is meant to be easy.

## Installation
Run the following to install:
```python
pip install py-easyDL
```
## Usage
EasyDL uses the same methodology as Google's Tensorflow v2.x. 
Here are some imports from our package.
```python
import easyDL
from easyDL.preprocessing.image import load_single_image,\
    load_images_from_directory, load_images_from_classes_directory
from easyDL.preprocessing.csv import load_csv
from easyDL.preprocessing.datasets import mnist, cifar10, cifar100
from easyDL.preprocessing.utils import shuffle, normalize
from easyDL.models import Model, load_model
from easyDL.activations import Tanh, Softmax, Sigmoid, ReLU, LeakyReLU, Step, Identity
from easyDL.layers import Dense, MaxPooling2D, Conv2D, Flatten, Dropout, BatchNorm
from easyDL.optimizers import GradientDescent, Adam, RMSProp, AdaGrad, MomentumGD, NesterovGD
from easyDL.visualization import plot_losses, plot_accuracy
from easyDL.losses import BinaryCrossEntropy, CategoricalCrossEntropy, \
    SparseCategoricalCrossEntropy, MeanSquaredError
from easyDL.evaluation import plot_evaluation_matrix, plot_confusion_matrix
```
This is an example using our package.
```python
# Preprocessing
(X_train, Y_train), (X_test, Y_test) = mnist.load_data()
X_train = normalize(X_train[:4000])
Y_train = Y_train[:4000]

X_test = normalize(X_test[:1000])
Y_test = Y_test[:1000]

# Create a model
model = Model()

# Adding layers
model.add(Conv2D(6, kernel_size= (5, 5), input_shape= X_train.shape[1:]))
model.add(BatchNorm())
model.add(ReLU())
model.add(MaxPooling2D())

model.add(Conv2D(16, kernel_size= (5, 5)))
model.add(BatchNorm())
model.add(ReLU())
model.add(MaxPooling2D())

model.add(Flatten())

model.add(Dense(120))
model.add(BatchNorm())
model.add(ReLU())

model.add(Dense(84))
model.add(BatchNorm())
model.add(ReLU())

model.add(Dense(10))
model.add(Softmax())

# Compiling the model
model.compile(loss= 'sparse_categorical_crossentropy', optimizer= Adam(lr= 0.01))

# Training the model
model.fit(X_train, Y_train, validation_data= (X_test, Y_test),
            epochs= 10, batch_size= 64, verbose= True)

# Plotting losses and accuracies
plot_losses(model)
plot_accuracy(model)

# Predicting labels using the model
predictions = model.predict(X_test)

# Plotting confusion matrix
plot_confusion_matrix(Y_test, predictions)

# Printing evaluation matrix
plot_evaluation_matrix(Y_test, predictions)

# Save the model into a .pkl file
model.save('PATH/TO/FILE.pkl')

# Load a saved .pkl model
model = load_model('PATH/TO/FILE.pkl')
```
