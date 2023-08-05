"""
MaxPooling2D Layer class.
"""
import numpy as np

class MaxPooling2D:
    """
    MaxPooling2D(pool_size= (2, 2), stride= 1)

    MaxPooling2D Layer class.

    Attributes
    ----------
    input_shape : int
        Dimensions of the input of the first layer of the network (Data dimensions).
    output_dim : int
        Output dimensions of the layer.
    """
    def __init__(self, pool_size= (2, 2), stride= 2):
        super().__init__()
        self._pool_size = pool_size

        if not isinstance(self._pool_size, tuple):
            self._pool_size = (self._pool_size, self._pool_size)
        else:
            if len(self._pool_size) == 2:
                if self._pool_size[0] != self._pool_size[1]:
                    raise ValueError('pool_size dimensions must be the same')
            else:
                raise ValueError('pool_size must have 2 dimensions')

        self._stride = stride
        self._a = None
        self._cache = {}
        self.type = 'MaxPooling2D'
        self.original_img_dim = None
        self.output_dim = None

    def __call__(self, input_dim):
        self.original_img_dim = input_dim
        self.output_dim = self._get_output_dim()

    def _get_output_dim(self):
        num, h_in, w_in, channels = self.original_img_dim
        h_pool, w_pool = self._pool_size
        h_out = 1 + (h_in - h_pool) // self._stride
        w_out = 1 + (w_in - w_pool) // self._stride
        return (num, h_out, w_out, channels)

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
        self._a = np.array(input_val, copy=True)
        num, h_in, w_in, channels = self._a.shape
        h_pool, w_pool = self._pool_size
        h_out = 1 + (h_in - h_pool) // self._stride
        w_out = 1 + (w_in - w_pool) // self._stride
        output = np.zeros((num, h_out, w_out, channels))

        for i in range(h_out):
            for j in range(w_out):
                h_start = i * self._stride
                h_end = h_start + h_pool
                w_start = j * self._stride
                w_end = w_start + w_pool
                a_prev_slice = input_val[:, h_start:h_end, w_start:w_end, :]
                self._save_mask(a_prev_slice, (i, j))
                output[:, i, j, :] = np.max(a_prev_slice, axis=(1, 2))
        return output

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
        output = np.zeros_like(self._a)
        _, h_out, w_out, _ = dout.shape
        h_pool, w_pool = self._pool_size

        for i in range(h_out):
            for j in range(w_out):
                h_start = i * self._stride
                h_end = h_start + h_pool
                w_start = j * self._stride
                w_end = w_start + w_pool
                output[:, h_start:h_end, w_start:w_end, :] = \
                    np.add(output[:, h_start:h_end, w_start:w_end, :],
                           dout[:, i:i + 1, j:j + 1, :] * self._cache[(i, j)],
                           casting= 'unsafe')
        return output

    def _save_mask(self, inp, cords):
        mask = np.zeros_like(inp)
        num, height, width, channels = inp.shape
        inp = inp.reshape((num, height * width, channels))
        idx = np.argmax(inp, axis=1)

        n_idx, c_idx = np.indices((num, channels))
        mask.reshape((num, height * width, channels))[n_idx, idx, c_idx] = 1
        self._cache[cords] = mask
