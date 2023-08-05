"""
Flatten layer class.
"""
import numpy as np

class Flatten:
    """
    Flatten()

    Flatten Layer class.
    """
    def __init__(self, input_shape= None):
        super().__init__()
        self.input_shape = input_shape
        self.type = 'Flatten'
        self.input_dim = None
        self.output_dim = None

    def __call__(self, input_dim):
        self.input_dim = input_dim
        # self.output_dim = 1
        # for i in range(1, len(input_dim)):
        #     self.output_dim *= i
        self.output_dim = input_dim[1]*input_dim[2]*input_dim[3]

    def forward(self, input_val):
        """
        Forward pass function.

        Parameters
        ----------
        input_val : np.ndarray
            a numpy array of input.

        Returns
        -------
        output : np.ndarray
            a numpy array of output.

        """
        self.input_dim = self.input_dim
        output = np.ravel(input_val).reshape(input_val.shape[0], -1)
        return output.T

    def backward(self, dout):
        """
        Backward pass function.

        Parameters
        ----------
        dout : np.ndarray
            a numpy array of input.

        Returns
        -------
        output : np.ndarray
            a numpy array of output.
        """
        output = dout.reshape(self.input_dim)
        return output
