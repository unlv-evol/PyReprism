import re
from PyReprism.utils import extension

class MarkUp:
    def __init__():
        pass

    @staticmethod
    def comment():
        
        return re.compile(r'(?P<multilinecomment><!--.*?-->)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"]*)', re.DOTALL | re.MULTILINE)
        
    @staticmethod
    def keywords() -> list:
        pass
    
    @staticmethod
    def file_extension():
        return extension.markup
    
    @staticmethod
    def remove_keywords(source: str):
        keywords = MarkUp.keywords()
        pattern = r'\b(' + '|'.join(keywords) + r')\b'
  
        return re.compile(pattern)


