import re
from PyReprism.utils import extension
class Rust:
    def __init__():
        pass

    @staticmethod
    def comment():
        pass

    @staticmethod
    def keywords() -> list:
        pass
        
    @staticmethod
    def file_extension():
        return extension.rust
    
    @staticmethod
    def remove_keywords(source: str):
        keywords = Rust.keywords()
        pattern = r'\b(' + '|'.join(keywords) + r')\b'
  
        return re.compile(pattern)