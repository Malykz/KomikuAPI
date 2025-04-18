class InvalidClient(Exception) :
    def __init__(self, message):
        super().__init__(message)

class YourInternetIsSucks(Exception) :        
    def __init__(self, message):
        super().__init__(message)