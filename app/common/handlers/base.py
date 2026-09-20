class BaseError(Exception):
    title: str
    status_code: int

    def __init__(self, details: str = '') -> None:
        self.details = details
