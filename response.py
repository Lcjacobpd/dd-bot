from enum import Enum


class ResponseCodes(Enum):
    success = 0
    error   = 1

class Response():
    # Properties
    ResponseCode: ResponseCodes
    Message: str
    BlockCount: int

    # Constructor
    def __init__(self, message: str="", blockcount: int=1, responseCode: ResponseCodes=ResponseCodes.success) -> None:
        self.ResponseCode = responseCode
        self.Message = message
        self.BlockCount = blockcount