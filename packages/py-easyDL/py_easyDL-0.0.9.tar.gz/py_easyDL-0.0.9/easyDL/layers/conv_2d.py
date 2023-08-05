"""
Conv2D class
"""
import numpy as np

class Conv2D:
    """
    Conv2D(num_filters, kernel_size= 3, stride= 1)

    Conv2D Layer class.

    Attributes
    ----------
    num_filters : int
    kernel_size : int or tuple
        ex. 2 or (2, 2)
    stride : int
    input_shape: tuple
    """
    def __init__(self, num_filters, kernel_size= (3, 3), stride= 1,
                 input_shape= None, padding= 'valid'):
        super().__init__()
        self.input_shape = input_shape
        self.num_filters = num_filters
        self._kernel_size = kernel_size
        self._stride = stride
        self._padding = padding
        self.type = 'Conv2D'
        self.image_dim = None
        self._weights = None
        self._biases = None
        self.output_dim = None
        self._a_prev = None
        self._dw = None
        self._db = None

    def __call__(self, image_dim):
        self.image_dim = image_dim
        scale = 1/np.maximum(1., (self.num_filters+self.image_dim[-1])/2.)
        limit = np.sqrt(3.0 * scale)
        self._weights = np.random.uniform(-limit, limit, size=(*self._kernel_size,
                                                               self.image_dim[-1],
                                                               self.num_filters))

        self._biases = np.random.uniform(-limit, limit, size=(self.num_filters))
        self.output_dim = self._calculate_output_dims(self.image_dim)

    def forward(self, input_val):
        """
        Backward pass function.

        Parameters
        ----------
        input_val : np.ndarray
            a numpy array of input.

        Returns
        -------
        output : np.ndarray
            a numpy array of output.
        """
        self._a_prev = np.array(input_val, copy=True)
        # print(input_val.shape)
        output_shape = self._calculate_output_dims(self._a_prev.shape)
        _, h_out, w_out, _ = output_shape
        h_f, w_f, _, _ = self._weights.shape
        pads = self._calculate_pad_dims()
        a_prev_pad = self._pad(self._a_prev, pads)
        output = np.zeros(output_shape)

        for i in range(h_out):
            for j in range(w_out):
                h_start = i * self._stride
                h_end = h_start + h_f
                w_start = j * self._stride
                w_end = w_start + w_f

                output[:, i, j, :] = np.sum(
                    a_prev_pad[:, h_start:h_end, w_start:w_end, :, np.newaxis] *
                    self._weights[np.newaxis, :, :, :],
                    axis=(1, 2, 3)
                )

        output += self._biases
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
        _, h_out, w_out, _ = dout.shape
        num, h_in, w_in, _ = self._a_prev.shape
        h_f, w_f, _, _ = self._weights.shape
        pads = self._calculate_pad_dims()
        a_prev_pad = self._pad(self._a_prev, pads)
        output = np.zeros_like(a_prev_pad)

        self._db = dout.sum(axis=(0, 1, 2)) / num
        self._dw = np.zeros_like(self._weights)

        for i in range(h_out):
            for j in range(w_out):
                h_start = i * self._stride
                h_end = h_start + h_f
                w_start = j * self._stride
                w_end = w_start + w_f

                output[:, h_start:h_end, w_start:w_end, :] = np.add(
                    output[:, h_start:h_end, w_start:w_end, :],
                    np.sum(
                        self._weights[np.newaxis, :, :, :, :] *
                        dout[:, i:i+1, j:j+1, np.newaxis, :],
                        axis=4
                        ), casting= 'unsafe'
                    )

                self._dw += np.sum(
                    a_prev_pad[:, h_start:h_end, w_start:w_end, :, np.newaxis] *
                    dout[:, i:i+1, j:j+1, np.newaxis, :],
                    axis=0
                )

        self._dw /= num
        return output[:, pads[0]:pads[0]+h_in, pads[1]:pads[1]+w_in, :]

    def optimize(self, optimizer):
        """
        This function performs the gradient descent update
        Args:
            optimizer: optimizer.
        """
        self._weights, self._biases = optimizer.update(self._weights, self._biases,
                                                       self._dw, self._db)

    def _calculate_output_dims(self, input_dims):
        """
        calculating output dimensions.

        Parameters
        ----------
        input_dims : tuple
            a tuple of input dimensions.

        Raises
        ------
        ValueError
            if `padding` is not 'same' or 'valid'..

        Returns
        -------
        tuple
            a tuple of output dimensions.

        """
        num, h_in, w_in, _ = input_dims
        h_f, w_f, _, n_f = self._weights.shape
        if self._padding == 'same':
            return (num, h_in, w_in, n_f)

        if self._padding == 'valid':
            h_out = (h_in - h_f) // self._stride + 1
            w_out = (w_in - w_f) // self._stride + 1
            return (num, h_out, w_out, n_f)
        raise ValueError("Unsupported padding value: {}".format(self._padding))

    def _calculate_pad_dims(self):
        """
        calculating pads.

        Raises
        ------
        ValueError
            if padding parameter is not 'same' or 'valid'.

        Returns
        -------
        tuple of integers
            a tuple of padding sizes.

        """
        if self._padding == 'same':
            h_f, w_f, _, _ = self._weights.shape
            return (h_f - 1) // 2, (w_f - 1) // 2

        if self._padding == 'valid':
            return 0, 0

        raise ValueError(f"Unsupported padding value: {self._padding}")


    def _pad(self, array, pads):
        """
        pad an array

        Parameters
        ----------
        array : np.ndarray
            a numpy array.
        pads : list
            list of pads.

        Returns
        -------
        np.ndarray
            a padded numpy array.

        """
        self._padding = self._padding
        return np.pad(array=array,
                      pad_width=((0, 0), (pads[0], pads[0]), (pads[1], pads[1]), (0, 0)),
                      mode='constant')
