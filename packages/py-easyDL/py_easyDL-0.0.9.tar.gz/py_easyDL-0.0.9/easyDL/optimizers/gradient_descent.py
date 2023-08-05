"""
Gradient Descent optimizer class
"""

from ._Optimizer import _Optimizer

class GradientDescent(_Optimizer):
    """
    Gradient descent algorithm updates the parameters by moving in the direction opposite
    to the gradient of the objective function with respect to the network parameters.

    Parameters
    ----------
    lr : float, optional
        the rate of change of the weights w.r.t their gradient. The default is 0.01.
    """
    def __init__(self, lr= 0.01):
        super().__init__()
        self.learning_rate = lr
        self.type = 'Gradient Descent'

    def update(self, w, b, dw, db):
        """
        update function.

        Parameters
        ----------
        w : np.ndarray
            weights numpy array of the layer.
        b : np.ndarray
            biases numpy array of the layer.
        dw : np.ndarray
            gradients of weights numpy array of the layer.
        db : np.ndarray
            gradients of biases numpy array of the layer.

        Returns
        -------
        w : np.ndarray
            updated weights numpy array of the layer.
        b : np.ndarray
            updated biases numpy array of the layer.

        """
        w = w - self.learning_rate * dw
        b = b - self.learning_rate * db.sum(axis= 0)
        return w, b
