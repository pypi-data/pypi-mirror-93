"""
Leaky Rectified Linear Unit (LeakyReLU) activation function.
"""
import numpy as np
from ._Activation import _Activation

class LeakyReLU(_Activation):
    """
    Leaky Rectified Linear Unit (LeakyReLU) activation function.

    Parameters
    ----------
    rate : float, optional
        The slope of the line from 0 to -inf. The default is 0.1.
    """
    def __init__(self, rate= 0.1):
        super().__init__()
        self.rate = rate
        self.type = 'LeakyReLU'
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
        self.out = np.where(input_val > 0, input_val, input_val * self.rate)
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
        dinp = np.ones_like(self.out)
        dinp[self.out <= 0] = self.rate
        return dout * dinp
