import re
from utils.file_extensions import FileExtension

class Bash:
    def __init__():
        pass

    @staticmethod
    def comment():
        # shell, bash
        pattern = re.compile(r'(?P<comment>#.*?$)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^#\'"]*)', re.DOTALL | re.MULTILINE)

        return pattern
        
    @staticmethod
    def file_extension() -> str:
        return FileExtension.bash