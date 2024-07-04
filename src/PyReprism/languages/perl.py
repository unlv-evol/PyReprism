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




