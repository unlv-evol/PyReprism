import re
from PyReprism.utils import extension

class Java:
    def __init__():
        pass

    @staticmethod
    def comment():
        pass
        
    @staticmethod
    def file_extension() -> str:
        return extension.java
    
    @staticmethod
    def keywords() -> list:
        pass

    @staticmethod
    def remove_comments(source: str) -> str:
        pass

    @staticmethod
    def remove_keywords(source: str):
        keywords = Java.keywords()
        pattern = r'\b(' + '|'.join(keywords) + r')\b'
  
        return re.compile(pattern)
