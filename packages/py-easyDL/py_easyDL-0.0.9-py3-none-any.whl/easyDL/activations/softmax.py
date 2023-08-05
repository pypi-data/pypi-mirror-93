"""
Softmax activation function class.
"""
import numpy as np
from ._Activation import _Activation

class Softmax(_Activation):
    """
    Softmax activation function.

    Parameters
    ----------
    No parameters needed.
    """
    def __init__(self):
        super().__init__()
        self.type = 'Softmax'
        self.out = None

    def forward(self, input_val):
        """
        Forward pass function.

        Parameters
        ----------
        input_val : np.ndarray
            inputs numpy array to the activation function.

        Returns
        -------
        np.ndarray
            outputs numpy array after applying the activation.

        """
        self.out = np.exp(input_val, dtype= np.float64) / \
            (np.sum(np.exp(input_val, dtype= np.float64),
                    axis=0, dtype= np.float64))
        return self.out

    def backward(self, dout):
        """
        Backward pass function

        Parameters
        ----------
        dJ : np.ndarray
            backpropagation inputs numpy array to the activation function.

        Returns
        -------
        np.ndarray
            backpropagation outputs numpy array to the activation function.

        """
        self.out = self.out
        return dout.T
