"""
AdaGrad optimizer class
"""

import numpy as np
from ._Optimizer import _Optimizer

class AdaGrad(_Optimizer):
    """
    The main motivation behind the AdaGrad was the idea of Adaptive Learning rate for
    different features in the dataset, i.e.instead of using the same learning rate across
    all the features in the dataset, we might need different learning rate for different features.

    Parameters
    ----------
    lr : float, optional
        the rate of change of the weights w.r.t their gradient. The default is 0.01.
    epsilon : float, optional
        a very small number added to the denominator while updating the weights to insure that
        it is not divided by zero. The default is 1e-8.
    """
    def __init__(self, lr=0.01, epsilon=1e-8):
        super().__init__()
        self.epsilon = epsilon
        self.learning_rate = lr
        self.type = 'AdaGrad'

    def update(self, w, b, dw, db):
        """
        update function.

        Parameters
        ----------
        w : np.ndarray
            weights numpy array of the layer.
        b : np.ndarray
            biases numpy array of the layer.
        dw : np.ndarray
            gradients of weights numpy array of the layer.
        db : np.ndarray
            gradients of biases numpy array of the layer.

        Returns
        -------
        w : np.ndarray
            updated weights numpy array of the layer.
        b : np.ndarray
            updated biases numpy array of the layer.

        """
        # *** weights *** #
        self.v_dw[self.counter] = self.v_dw[self.counter] + (dw**2)

        # *** biases *** #
        self.v_db[self.counter] = self.v_db[self.counter] + (db**2)

        ## update weights and biases
        w = w - self.learning_rate*(dw/(np.sqrt(self.v_dw[self.counter])+self.epsilon))
        b = b - self.learning_rate*(db/(np.sqrt(self.v_db[self.counter])+self.epsilon))

        self.counter = (self.counter + 1) % self.num_layers

        return w, b
