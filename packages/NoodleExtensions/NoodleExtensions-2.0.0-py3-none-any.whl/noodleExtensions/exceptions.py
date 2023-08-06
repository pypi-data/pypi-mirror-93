class NoteNotFoundError(Exception):

    def __init__(self, message="The Specified note couldn't be found"):
        super().__init__(message)

class WallNotFoundError(Exception):
    
    def __init__(self, message="The Specified wall couldn't be found"):
        super().__init__(message)

class TooManyNotes(Exception):
    
    def __init__(self, message="The specified note returned too many notes"):
        super().__init__(message)

class TooManyWalls(Exception):
    
    def __init__(self, message="The specified wall returned too many walls"):
        super().__init__(message)
