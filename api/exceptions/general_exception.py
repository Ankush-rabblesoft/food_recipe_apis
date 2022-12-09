from email import message
from api.exceptions.base_exception import IException


class GeneralException(IException):
    code = 422
    
    def __init__(self, *args):
        
        self.message = args[0]

        super(IException, self).__init__(*args)
