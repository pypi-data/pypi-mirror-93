"""
Rectified Linear Unit (ReLU) activation function.
"""
import numpy as np
from ._Activation import _Activation

class ReLU(_Activation):
    """
    Rectified Linear Unit (ReLU) activation function.

    Parameters
    ----------
    No parameters needed.
    """
    def __init__(self):
        super().__init__()
        self.type = 'ReLU'
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
        self.out = np.maximum(0, input_val)
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
        dinp = np.array(dout, copy=True)
        dinp[self.out <= 0] = 0
        return dinp
