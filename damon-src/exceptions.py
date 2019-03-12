

# error for when the wrong data source in entered
class InvalidSourceError:

    def __init__(self, message):
        print(f'InvalidSourceError:  + {message}')


# error for when the wrong data source in entered
class InvalidModelError:

    def __init__(self, message):
        print(f'InvalidModelError:  + {message}')


# error for when in comparable datasets are used
class InvalidCorrelationFormattingError:

    def __init__(self, message):
        print(f'InvalidCorrelationFormattingError: + {message}')
