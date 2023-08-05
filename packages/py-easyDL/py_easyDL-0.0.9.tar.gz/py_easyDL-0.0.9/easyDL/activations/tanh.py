"""
Tanh activation function.
"""

import numpy as np
from ._Activation import _Activation

class Tanh(_Activation):
    """
    Tanh activation function.

    Parameters
    ----------
    No parameters needed.
    """
    def __init__(self):
        super().__init__()
        self.type = 'Tanh'
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
        self.out = np.tanh(input_val)
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
        tanh = self.out
        return dout * (1.0 - tanh**2)
