import os
from Email import Email

class EmailParser:

    def parseTxt(self, filePath):
        pass


    def parseEml(self, filePath):
        pass
    
    def parse(self, filePath) -> Email:
        if filePath is None:
            raise ValueError("File path cannot be None")
        if not os.path.exists(filePath):
            raise FileNotFoundError("The file doesn't exist")
        if not os.path.isfile(filePath):
            raise ValueError("The path doesn't lead to file")
        
        fileExtension = os.path.splitext(filePath)[1].lower()
        if fileExtension == ".txt":
            pass
        elif fileExtension == ".eml":
            pass
        else:
            raise ValueError("Invalid file extension, must be .txt or .eml")