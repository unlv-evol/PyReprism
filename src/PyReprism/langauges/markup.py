import re
from PyReprism.utils.extensions import FileExtension

class MarkUp:
    def __init__():
        pass

    @staticmethod
    def comment():
        
        return re.compile(r'(?P<multilinecomment><!--.*?-->)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"]*)', re.DOTALL | re.MULTILINE)
        
    
    @staticmethod
    def file_extension():
        return FileExtension.markup


