class Config:
    def __init__(self):
        self.session_key = None
        self.client = None
        self.client_name = None

    def update(self, session_key, client,client_name):
        self.session_key = session_key
        self.client = client
        self.client_name = client_name

config = Config()