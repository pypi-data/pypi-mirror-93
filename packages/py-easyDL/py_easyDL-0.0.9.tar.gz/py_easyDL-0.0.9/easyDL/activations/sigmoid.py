"""
Sigmoid activation function class.
"""
import numpy as np
from ._Activation import _Activation

class Sigmoid(_Activation):
    """
    Sigmoid activation function.

    Parameters
    ----------
    No parameters needed.
    """
    def __init__(self):
        super().__init__()
        self.type = 'Sigmoid'
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
        self.out = 1 / (1 + np.exp(-input_val))
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
        sig = self.out
        return dout * sig * (1 - sig)
