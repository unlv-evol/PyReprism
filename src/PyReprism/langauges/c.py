import re
from utils.file_extensions import FileExtension

class C:
    def __init__():
        pass

    @staticmethod
    def comment():
    
        full_regex = (r'(?P<comment>//.*?$|[{}]+)|(?P<multilinecomment>/\*.*?\*/)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"]*)')

        partial_comment_regex = (r'(?P<comment>/\*.*?$|^.*?\*/)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"{}]*)')
        
        # Combine both regexes
        pattern = f"{full_regex}|{partial_comment_regex}"
        
        return re.compile(pattern, re.DOTALL | re.MULTILINE)
        
    
    @staticmethod
    def file_extension():
        return FileExtension.c