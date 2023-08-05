"""
BatchNorm Layer class.
"""
import numpy as np

class BatchNorm:
    """
    BatchNorm()

    BatchNorm Layer class.
    """
    def __init__(self):
        super().__init__()
        self.type = 'BatchNorm'
        self.input_dim = None
        self.output_dim = None
        self._weights = None
        self._biases = None
        self._a_prev = None
        self._mu = None
        self._var = None
        self.x_norm = None
        self._dw = None
        self._db = None

    def __call__(self, input_dim):
        self.input_dim = input_dim
        self.output_dim = input_dim
        if  isinstance(self.input_dim, int):
            shape = (self.input_dim, 1)
            scale = 1/np.maximum(1., self.input_dim)
        else:
            shape = (1, 1, 1, self.input_dim[-1])
            scale = 1/np.maximum(1., self.input_dim[-1])

        limit = np.sqrt(3.0 * scale)
        self._weights = np.random.uniform(-limit, limit, size=shape)
        self._biases = np.random.uniform(-limit, limit, size=shape)

    def forward(self, input_val):
        """
        Forward pass function

        Parameters
        ----------
        input_val : np.ndarray
            a numpy array of input.

        Returns
        -------
        out : np.ndarray
            a numpy array of output.

        """
        self._a_prev = np.array(input_val, copy=True)

        if len(input_val.shape) == 2:
            self._mu = np.mean(input_val,axis=(0))
            self._var = np.var(input_val,axis=(0))
        else:
            self._mu = np.mean(input_val,axis=(0, 2, 3), keepdims=True)
            self._var = np.var(input_val,axis=(0, 2, 3), keepdims=True)

        self.x_norm = (input_val - self._mu) / np.sqrt(self._var + 1e-8)
        out = self._weights * self._a_prev + self._biases

        return out

    def backward(self, dout):
        """
        Backward pass function

        Parameters
        ----------
        dout : np.ndarray
            a numpy array of input.

        Returns
        -------
        dinp : np.ndarray
            a numpy array of output.

        """
        num = self._a_prev.shape[0]

        x_mu = self._a_prev - self._mu
        std_inv = 1. / np.sqrt(self._var + 1e-8)

        dx_norm = dout * self._weights
        dvar = np.sum(dx_norm * x_mu, axis=0) * -.5 * std_inv**3
        dmu = np.sum(dx_norm * -std_inv, axis=0) + dvar * np.mean(-2. * x_mu, axis=0)

        dinp = (dx_norm * std_inv) + (dvar * 2 * x_mu / num) + (dmu / num)
        self._dw = np.sum(dout * self.x_norm, axis=0)
        self._db = np.sum(dout, axis=0)

        return dinp
