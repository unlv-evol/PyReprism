import re
from PyReprism.utils import extension

class PHP:
    def __init__():
        pass

    @staticmethod
    def comment():
        pattern = re.compile(r'(?P<comment>#.*?$|//.*?$|[{}]+)|(?P<multilinecomment>/\*.*?\*/)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^#/\'"{}]*)', re.DOTALL | re.MULTILINE)

        return pattern
    
    @staticmethod
    def keywords() -> list:
        pass
    
    @staticmethod
    def file_extension():
        return extension.php
