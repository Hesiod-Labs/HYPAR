

# error for when the wrong data source in entered
class InvalidDatasetException(BaseException):

    def __init__(self, message):
        print(f'InvalidDatasetException:  + {message}')


class SourceException(BaseException):

    def __init__(self, message):
        print(f'InvalidSourceException:  + {message}')


class DataExistsException(BaseException):

    def __init__(self, message):
        print(f'DataExistsException:  + {message}')
