"""
Momentum Gradient Descent optimizer class
"""

from ._Optimizer import _Optimizer

class MomentumGD(_Optimizer):
    """
    In Momentum GD, we are moving with an exponential decaying cumulative average of
    previous gradients and current gradient.

    Attributes
    ----------
    lr : float, optional
        the rate of change of the weights w.r.t their gradient. The default is 0.01.
    gamma : float, optional
        The default is 0.9.
    """
    def __init__(self, lr=0.01, gamma=0.9):
        super().__init__()
        self.gamma = gamma
        self.learning_rate = lr
        self.type = 'Nesterov GD'

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
        # *** weights *** #
        self.v_dw[self.counter] = self.gamma * self.v_dw[self.counter] + self.learning_rate * dw

        # *** biases *** #
        self.v_db[self.counter] = self.gamma * self.v_db[self.counter] + self.learning_rate * db

        ## update weights and biases
        w = w - self.v_dw[self.counter]
        b = b - self.v_db[self.counter]

        self.counter = (self.counter + 1) % self.num_layers

        return w, b
