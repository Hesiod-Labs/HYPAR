

# exception for when the Topic instance cannot be instantiated due to a gap in the list
class TopicTitleError(BaseException):

    def __init__(self, message):
        print(f'TopicTitleError:  + {message}')

# exception for when the wrong model type is attempted to be used
class ImproperModelError(BaseException):

    def __init__(self, message):
        print(f'ImproperModelError:  + {message}')
