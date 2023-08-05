"""
Abstract Activation class.
"""
class _Activation:
    def __init__(self):
        super().__init__()
        self.type = None
        self._weights = None
        self._biases = None
        self.output_dim = None
        self.input_dim = None

    def __str__(self):
        return "{} Layer".format(self.type)

    def __call__(self, input_dim):
        self.output_dim = input_dim
        self.input_dim = input_dim
