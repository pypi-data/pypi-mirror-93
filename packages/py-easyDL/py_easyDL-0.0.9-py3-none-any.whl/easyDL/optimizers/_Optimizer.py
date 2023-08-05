class _Optimizer:
    def __init__(self):
        super().__init__()
        self.num_layers = None
        self.v_dw = None
        self.v_db = None
        self.m_dw = None
        self.m_db = None
        self.lr_updated = None
        self.counter = None
    
    def set_num_layers(self, num_layers):
        self.num_layers = num_layers
        self.v_dw = [0]*num_layers
        self.v_db = [0]*num_layers
        self.m_dw = [0]*num_layers
        self.m_db = [0]*num_layers
        self.lr_updated = [0]*num_layers
        self.counter = 0
        
    def update(self, w, b, dw, db):
        pass