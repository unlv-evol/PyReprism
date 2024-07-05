import re
from PyReprism.utils import extension

class Perl:
    def __init__():
        pass

    @staticmethod
    def comment():
         
        # PERL
        pattern = re.compile(r'(?P<comment>#.*?$|[{}]+)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^#\'"{}]*)', re.DOTALL | re.MULTILINE)
        
        return pattern
        
    @staticmethod
    def keywords() -> list:
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.perl
    
    @staticmethod
    def remove_keywords(source: str):
        keywords = Perl.keywords()
        pattern = r'\b(' + '|'.join(keywords) + r')\b'
  
        return re.compile(pattern)




