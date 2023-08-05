"""
Sparse Categorical Crossentropy class.
"""
import numpy as np

def one_hot_encoding(targets):
    """
    Get one hot encoding matrix of an array.

    Parameters
    ----------
    targets : np.ndarray
        labels numpy array.
    num_classes : int
        number of classes in labels numpy array.

    Returns
    -------
    ind : TYPE
        DESCRIPTION.

    """
    num = len(targets)
    num_classes = len(set(targets))
    ind = np.zeros((num, num_classes))
    for i in range(num):
        ind[i, targets[i]] = 1
    return ind

class SparseCategoricalCrossEntropy:
    """
    Sparse Categorical Crossentropy loss function class.

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
        self.type = 'Sparse Categorical Cross-Entropy'
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
        return -np.mean(one_hot_encoding(self.real) * np.log(self.predicted+1e-8))

    def backward(self):
        """
        Backward pass function.

        Returns
        -------
        np.ndarray
            a numpy array of the derivative of the loss.
        """
        return self.predicted - one_hot_encoding(self.real)
