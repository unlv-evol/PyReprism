import re
from utils.file_extensions import FileExtension

class Perl:
    def __init__():
        pass

    @staticmethod
    def comment():
         
        # PERL
        pattern = re.compile(r'(?P<comment>#.*?$|[{}]+)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^#\'"{}]*)', re.DOTALL | re.MULTILINE)
        
        return pattern
        
    
    @staticmethod
    def file_extension():
        return FileExtension.perl




