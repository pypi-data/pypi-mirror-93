"""
Mean Squared Error class.
"""
import numpy as np

class MeanSquaredError:
    """
    Categorical Crossentropy loss function class.

    Parameters
    ----------
    pred : np.ndarray, optional
        predictions numpy array.
    real : np.ndarray, optional
        targets numpy array.

    Returns
    -------
    None.

    """
    def __init__(self, pred= None, real= None):
        super().__init__()
        self.type = 'Mean Squared Error'
        self.predicted = pred
        self.real = real

    def forward(self):
        """
        Calculating the loss.

        Returns
        -------
        np.ndarray
            Total loss.

        """
        return np.power(self.predicted - self.real, 2).mean()

    def backward(self):
        """
        Backward pass function.

        Returns
        -------
        np.ndarray
            a numpy array of the derivative of the loss.

        """
        return 2 * (self.predicted - self.real).mean()
