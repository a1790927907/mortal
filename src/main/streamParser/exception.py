class StreamParserException(Exception):
    def __init__(self, message: str, error_code: int = 500, **json_kwargs):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.json_kwargs = json_kwargs
