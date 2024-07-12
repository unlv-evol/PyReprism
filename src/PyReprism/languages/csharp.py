import re
from PyReprism.utils import extension

class CSharp:
    def __init__():
        pass

    @staticmethod
    def comment():
        return re.compile(r'//.*|/\*[\s\S]*?\*/')

    @staticmethod
    def remove_comments(source: str) -> str:
        return re.sub(CSharp.comment, '', source);

    @staticmethod
    def keywords():
        pass
    
    @staticmethod
    def file_extension():
        return extension.ruby
    
    @staticmethod
    def remove_keywords(source: str):
        keywords = CSharp.keywords()
        pattern = r'\b(' + '|'.join(keywords) + r')\b'
  
        return re.sub(re.compile(pattern), '', source)