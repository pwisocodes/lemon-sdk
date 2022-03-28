class BaseError(Exception):
    detail = None

    def __init__(self, detail: str):
        self.detail = detail

    def to_representation(self):
        return self.detail

    def __str__(self):
        return self.to_representation()

    def __repr__(self):
        return self.to_representation()


class RestApiError(BaseError):
    pass


class StreamError(BaseError):
    pass

class OrderStatusError(BaseError):
    pass

class LemonMarketError(BaseError):
    error_code: str
    error_message: str

    def __init__(self, error_code: str, error_message):
        super().__init__(f"{error_code}: {error_message}")