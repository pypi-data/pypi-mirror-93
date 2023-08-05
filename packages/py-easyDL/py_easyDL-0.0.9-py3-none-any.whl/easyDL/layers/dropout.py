"""
Dropout layer class.
"""
import numpy as np

class Dropout:
    """
    Dropout(rate= 0.1)

    Dropout Layer class.

    Attributes
    ----------
    rate: float -> [0, 1[
        probability that given unit will not be dropped out
    """
    def __init__(self, rate= 0.1):
        super().__init__()
        self._rate = rate
        self.type = 'Flatten'
        self._mask = None
        self.output_dim = None

    def __call__(self, input_dim):
        self.output_dim = input_dim

    def _apply_mask(self, array, mask):
        array *= mask
        array /= self._rate
        return array

    def forward(self, input_val, training= True):
        """
        Forward pass function.

        Parameters
        ----------
        input_val : np.ndarray
            a numpy array of input.
        training : bool, optional
            Whether dropout layer should be training or not. The default is True.

        Returns
        -------
        out_masked : np.ndarray
            a numpy array of output.

        """
        if training:
            self._mask = (np.random.rand(*input_val.shape) < self._rate)
            out_masked = self._apply_mask(input_val, self._mask)
            return out_masked
        return input_val

    def backward(self, dout):
        """
        Backward pass function.

        Parameters
        ----------
        dout : np.ndarray
            a numpy array of input.

        Returns
        -------
        out_masked : np.ndarray
            a numpy array of output.
        """
        out_masked = self._apply_mask(dout, self._mask)
        return out_masked
