"""
Categorical Crossentropy class.
"""
import numpy as np

class CategoricalCrossEntropy:
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
        self.type = 'Categorical Cross-Entropy'
        self.predicted = np.transpose(pred)
        self.real = real

    def forward(self):
        """
        Calculating the loss.

        Returns
        -------
        np.ndarray
            Total loss.

        """
        return -np.mean(self.real*np.log(self.predicted))

    def backward(self):
        """
        Backward pass function.

        Returns
        -------
        np.ndarray
            a numpy array of the derivative of the loss.

        """
        return self.predicted - self.real
