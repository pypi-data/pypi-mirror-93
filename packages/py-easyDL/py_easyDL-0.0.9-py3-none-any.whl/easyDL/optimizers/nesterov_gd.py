"""
Nesterov Gradient Descent optimizer class
"""

from ._Optimizer import _Optimizer

class NesterovGD(_Optimizer):
    """
    In Nesterov Accelerated Gradient Descent we are looking forward to seeing whether
    we are close to the minima or not before we take another step based on the current gradient
    value so that we can avoid the problem of overshooting.

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
        w_temp = w - self.gamma * self.v_dw[self.counter]
        dw_temp = dw - self.gamma * self.v_dw[self.counter]
        w = w_temp - self.learning_rate * dw_temp
        self.v_dw[self.counter] = self.gamma * self.v_dw[self.counter] + \
            self.learning_rate * dw_temp

        # *** biases *** #
        b_temp = b - self.gamma * self.v_db[self.counter]
        db_temp = db - self.gamma * self.v_db[self.counter]
        b = b_temp - self.learning_rate * db_temp
        self.v_db[self.counter] = self.gamma * self.v_db[self.counter] + \
            self.learning_rate * db_temp

        self.counter = (self.counter + 1) % self.num_layers

        return w, b
