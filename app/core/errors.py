class NotFoundError(Exception):
    def __init__(self, detail: str = "ressource not found"):
        self.detail = detail

class ConflictError(Exception):
    def __init__(self, detail: str = "conflict"):
        self.detail = detail