import re
from PyReprism.utils import extension

class MarkDown:
    def __init__():
        pass

    @staticmethod
    def comment():

        return re.compile(r'(?P<multilinecomment><!--.*?-->)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"]*)', re.DOTALL | re.MULTILINE)
        
    @staticmethod
    def remove_comments(source: str):
        return re.sub(MarkDown.comment, '', source)
    
    @staticmethod
    def file_extension():
        return extension.markdown
    
    @staticmethod
    def keywords() -> list:
        pass

    @staticmethod
    def remove_keywords(source: str):
        keywords = MarkDown.keywords()
        pattern = r'\b(' + '|'.join(keywords) + r')\b'
  
        return re.sub(re.compile(pattern), '', source)

