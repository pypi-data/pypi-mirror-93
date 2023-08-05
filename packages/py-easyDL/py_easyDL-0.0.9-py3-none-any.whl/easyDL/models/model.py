"""
Model class
"""
from time import sleep
import pickle
from os import remove
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib
import easyDL
from easyDL.losses import BinaryCrossEntropy, MeanSquaredError,\
    CategoricalCrossEntropy, SparseCategoricalCrossEntropy
from easyDL.optimizers import GradientDescent, Adam, AdaGrad,\
    MomentumGD, NesterovGD, RMSProp
from .load_model import load_model

def get_argmax(inp):
    """
    get index of maximum value in array
    """
    return np.argmax(inp, axis= 0)

def normalize(inp):
    """
    normalize input array
    """
    out = inp - np.mean(inp)
    out = out / (np.std(inp) + 1e-8)
    return out

class Model:
    """

    A model class.

    Parameters
    ----------
    layers : list, optional
        a list containing the model's layers in sequence. The default is [].

    Returns
    -------
    an instance of the model.

    Methods
    -------
    add(layer):
        Adding a layer to the sequence of model's layers.

    """
    def __init__(self, layers= None):
        if layers is None:
            self.layers = []
        else:
            self.layers = layers
        self.losses = []
        self.losses_val = []
        self.acc = []
        self.acc_val = []
        self.optimized_layers= ['Dense', 'Conv2D']
        self.loss_fn = None
        self.loss_fn_name = None
        self.optimizer = None
        self.batch_size = None
        self.validation_data = None
        self.best_val_acc = None
        self.is_loss_legend_shown = False
        self.is_accuracy_legend_shown = False

    def add(self, layer):
        '''

        Parameters
        ----------
        layer : Layer class instance
            Adding a layer to the sequence of model's layers.

        Returns
        -------
        None.

        '''
        self.layers.append(layer)

    def save(self, path):
        '''


        Parameters
        ----------
        path : string
            The path for saving the model.

        Returns
        -------
        None.

        Examples
        -------


        '''
        with open(path, 'wb') as file:
            pickle.dump(self, file)

    def _live_update(self, name, epochs, epoch, loss, val_loss, acc, val_acc):
        if name == 'loss':
            if not self.is_loss_legend_shown:
                plt.figure(figsize= (12, 10))
        else:
            if not self.is_accuracy_legend_shown:
                plt.figure(figsize= (12, 10))
        matplotlib.use('Qt5Agg')
        if name == 'loss':
            plt.axis([0.5, epochs+0.5, np.min(self.losses)-0.05, np.max(self.losses)+0.05])
            plt.title('Loss live update', fontsize= 24)
            plt.xlabel('Epoch', fontsize= 20)
            plt.ylabel('Loss', fontsize= 20)
            plt.xticks(np.arange(1, epochs+1, 1), fontsize= 14)
            plt.yticks(fontsize= 14)
            plt.scatter(epoch+1, loss, c= '#4DD0E1', label= 'Training loss')
            if not val_loss is None:
                plt.scatter(epoch+1, val_loss, c= 'orange', label= 'Validation loss')
            if not self.is_loss_legend_shown:
                plt.legend()
                self.is_loss_legend_shown = True
        else:
            plt.axis([0.5, epochs+0.5, 0, 1])
            plt.title('Accuracy live update', fontsize= 24)
            plt.xlabel('Epoch', fontsize= 20)
            plt.ylabel('accuracy', fontsize= 20)
            plt.xticks(np.arange(1, epochs+1, 1), fontsize= 14)
            plt.yticks(fontsize= 14)
            plt.scatter(epoch+1, acc, c= '#4DD0E1', label= 'Training accuracy')
            if not val_acc is None:
                plt.scatter(epoch+1, val_acc, c= 'orange', label= 'Validation accuracy')
            if not self.is_accuracy_legend_shown:
                plt.legend(loc= 'upper left')
                self.is_accuracy_legend_shown = True
        plt.pause(0.5)

    def _forward_pass(self, inputs):
        for i in range(len(self.layers)):
            forward = self.layers[i].forward(inputs)
            inputs = forward
        return forward, inputs

    def _compute_loss(self, forward, targets):
        # print(forward)
        if self.loss_fn_name == 'binary_crossentropy':
            bce = BinaryCrossEntropy(forward, targets)
        elif self.loss_fn_name == 'categorical_crossentropy':
            bce = CategoricalCrossEntropy(forward, targets)
        elif self.loss_fn_name == 'mse':
            bce = MeanSquaredError(forward, targets)
        elif self.loss_fn_name == 'sparse_categorical_crossentropy':
            bce = SparseCategoricalCrossEntropy(forward, targets)
        else:
            raise ValueError('No Loss functions with that name.')

        return bce

    def _predict(self, inputs_val):
        # Forward pass
        forward_val, _ = self._forward_pass(inputs_val)

        if self.loss_fn_name == 'binary_crossentropy':
            return forward_val, forward_val

        if self.loss_fn_name == 'categorical_crossentropy' or \
            self.loss_fn_name == 'sparse_categorical_crossentropy':
            return get_argmax(forward_val), forward_val

    def predict(self, inputs):
        '''
        predicting the labels of the given data.

        Parameters
        ----------
        X : np.ndarray
            A numpy array of inputs to get predictions of from the trained model.

        Returns
        -------
        np.ndarray
            A numpy array of the predictions.

        '''
        # Forward pass
        forward, _ = self._forward_pass(inputs)

        if self.loss_fn_name == 'binary_crossentropy':
            return forward

        if self.loss_fn_name == 'categorical_crossentropy' or \
            self.loss_fn_name == 'sparse_categorical_crossentropy':
            return get_argmax(forward)

    def compile(self, loss, optimizer= 'rmsprop'):
        """
        compiling the model before training

        Parameters
        ----------
        loss : string or loss class instance
            the loss function used to compute loss.
        optimizer : string or optimizer class instance
            the optimizer used to update the weights.

        Returns
        -------
        None.

        """
        if isinstance(loss, str):
            self.loss_fn_name = loss
        else:
            if isinstance(loss, BinaryCrossEntropy):
                self.loss_fn_name = 'binary_crossentropy'
            elif isinstance(loss, CategoricalCrossEntropy):
                self.loss_fn_name = 'categorical_crossentropy'
            elif isinstance(loss, SparseCategoricalCrossEntropy):
                self.loss_fn_name = 'sparse_categorical_crossentropy'
            elif isinstance(loss, MeanSquaredError):
                self.loss_fn_name = 'mse'
            else:
                raise ValueError('The loss function must be a string\
                                 or an instance of a loss class.')

        if isinstance(optimizer, str):
            if optimizer == 'gradient_descent' or optimizer.lower() == 'sgd':
                self.optimizer = GradientDescent()
            elif optimizer.lower() == 'adam':
                self.optimizer = Adam()
            elif optimizer.lower() == 'ada_grad' or optimizer.lower() == 'adagrad':
                self.optimizer = AdaGrad()
            elif optimizer.lower() == 'rms_prop' or optimizer.lower() == 'rmsprop':
                self.optimizer = RMSProp()
            elif optimizer.lower() == 'nesterov_gd' or optimizer.lower() == 'nesterovgd':
                self.optimizer = NesterovGD()
            elif optimizer.lower() == 'momentum_gd' or optimizer.lower() == 'momentumgd':
                self.optimizer = MomentumGD()
            else:
                raise ValueError('Optimizer is not recognized')
        else:
            self.optimizer = optimizer

    def fit(self, x_train, y_train, epochs, batch_size= 32, validation_data= None,
              verbose= True, monitor_live_updates= None, restore_best_weights= False):
        """
        Train the model on training data

        Parameters
        ----------
        X_train : np.ndarray
            the data numpy array.
        Y_train : np.ndarray
            the labels numpy array.
        epochs : int
            number of epochs/iterations.
        batch_size : int, optional
            The size of each batch of data to train on. The default is 32.
        validation_data : tuple, optional
            Validation data. The default is None.
        verbose : bool, optional
            showing a progress bar for each epoch. The default is True.
        monitor_live_updates : 'string', optional
            live plotting of losses/accuracies for each epoch. The default is None.
        restore_best_weights : bool, optional
            restoring best weights upon best validation accuracy. The default is False.

        Returns
        -------
        None.

        """
        self.batch_size = batch_size
        self.validation_data = validation_data

        num_batches = x_train.shape[0] // self.batch_size

        num_optimized_layers = 0
        for i in range(len(self.layers)):
            layer = self.layers[i]
            if layer.type in self.optimized_layers:
                num_optimized_layers += 1

            if i == 0:
                if not layer.input_shape is None:
                    if layer.type == 'Conv2D':
                        x_train = normalize(x_train)
                        layer.input_shape = (self.batch_size,*layer.input_shape)
                    layer(layer.input_shape)
                else:
                    raise ValueError('First layer should have input shape')

            else:
                layer(self.layers[i-1].output_dim)

        self.optimizer.set_num_layers(num_optimized_layers)

        self.best_val_acc = 0
        cached_model_path = easyDL.__file__.split('__init__')[0] + 'models/cached_model.pkl'

        for epoch in range(epochs):
            if verbose:
                if epoch % 1 == 0:
                    print('Epoch {}/{}:'.format(epoch+1, epochs))
            sleep(1)
            for i in tqdm(range(num_batches), position=0, leave=True):
                inputs = x_train[i*self.batch_size: (i+1) * self.batch_size]
                labels = y_train[i*self.batch_size: (i+1) * self.batch_size]
                if self.layers[0].type == 'Dense':
                    inputs = np.transpose(inputs)
                loss, acc, val_loss, val_acc = self._run_epoch(inputs, labels, self.optimizer)

            self.losses.append(loss)
            self.acc.append(acc)

            if not monitor_live_updates is None:
                if monitor_live_updates == 'loss':
                    self._live_update('loss', epochs, epoch, loss, val_loss, acc, val_acc)
                elif monitor_live_updates == 'accuracy':
                    self._live_update('accuracy', epochs, epoch, loss, val_loss, acc, val_acc)

            if len(validation_data) != 0:
                self.losses_val.append(val_loss)
                self.acc_val.append(val_acc)

            if restore_best_weights:
                if val_acc > self.best_val_acc:
                    self.best_val_acc = val_acc
                    self.save(cached_model_path)

            if verbose:
                if epoch % 1 == 0:
                    print('\nLoss: {:.4f} \t Accuracy: {:.3f}'.format(loss, acc))
                    if not val_loss is None and not val_acc is None:
                        print('Val_Loss: {:.4f} \t Val_Accuracy: {:.3f}\n'.format(val_loss,
                                                                                  val_acc))

        if restore_best_weights:
            mod = load_model(cached_model_path)
            print(mod)
            remove(cached_model_path)

    def _run_epoch(self, inputs, labels, opt):

        forward, inputs = self._forward_pass(inputs)

        # Compute loss and first gradient
        bce = self._compute_loss(forward, labels)

        acc = 0
        if self.loss_fn_name == 'binary_crossentropy':
            acc = np.mean(np.around(forward).astype(np.int64) == labels)
        elif self.loss_fn_name == 'categorical_crossentropy' or \
            self.loss_fn_name == 'sparse_categorical_crossentropy':
            index = get_argmax(forward)
            acc = np.mean(index.astype(np.int64) == labels)

        loss = bce.forward()

        gradient = bce.backward()

        # Backpropagation
        for i, _ in reversed(list(enumerate(self.layers))):
            layer = self.layers[i]
            gradient = layer.backward(gradient)
            if layer.type in self.optimized_layers:
                layer.optimize(opt)

        acc_val = None
        loss_val = None
        if self.validation_data is not None:
            x_val = self.validation_data[0]
            y_val = self.validation_data[1]
            preds, forward_val = self._predict(x_val)
            acc_val = np.mean(preds == y_val)
            bce_val = self._compute_loss(forward_val, y_val)
            loss_val = bce_val.forward()

        return loss, acc, loss_val, acc_val
