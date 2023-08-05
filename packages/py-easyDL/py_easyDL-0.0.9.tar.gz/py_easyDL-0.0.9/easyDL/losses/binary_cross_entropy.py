"""
Binary Crossentropy class.
"""
import numpy as np

class BinaryCrossEntropy:
    """
    Binary Crossentropy loss function class.

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
    def __init__(self, pred= 0, real= 0):
        super().__init__()
        self.type = 'Binary Cross-Entropy'
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
        num = len(self.real)
        loss = np.nansum(-self.real * np.log(self.predicted) - \
                         (1 - self.real) * np.log(1 - self.predicted)) / num

        return np.squeeze(loss)

    def backward(self):
        """
        Backward pass function.

        Returns
        -------
        np.ndarray
            a numpy array of the derivative of the loss.

        """
        num = len(self.real)
        return (-(self.real / self.predicted) + ((1 - self.real) / (1 - self.predicted))) / num
