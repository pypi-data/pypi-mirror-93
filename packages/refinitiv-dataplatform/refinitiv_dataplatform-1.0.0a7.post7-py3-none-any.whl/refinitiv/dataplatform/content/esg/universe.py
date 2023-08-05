from .esg import ESG


class Definition:
    def __init__(self, session=None, closure=None, on_response=None):
        self.session = session
        self.closure = closure
        self.on_response = on_response

    def get_data(self):
        esg = ESG(session=self.session, on_response=self.on_response)
        return esg._get_universe(closure=self.closure)
