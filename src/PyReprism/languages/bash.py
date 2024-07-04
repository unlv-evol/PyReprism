import re
from PyReprism.utils import extension

class Bash:
    def __init__():
        pass

    @staticmethod
    def comment():
        # shell, bash
        pattern = re.compile(r'(?P<comment>#.*?$)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^#\'"]*)', re.DOTALL | re.MULTILINE)

        return pattern
    
    @staticmethod
    def keywords() -> str:
        pass
        
    @staticmethod
    def file_extension() -> str:
        return extension.bash