import re
from PyReprism.utils import extension

class Ruby:
    def __init__():
        pass

    @staticmethod
    def comment():
    
        # Ruby, GEMFILE
        full_regex = (r'(?P<comment>#.*?$)|(?P<multilinecomment>=begin.*?=end)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^#=\'"]*)', re.DOTALL | re.MULTILINE)
        partial_comment_regex = re.compile(r'(?P<comment>=begin.*?$|^.*?=end)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^#=\'"]*)', re.DOTALL)
        
        # Combine both regexes
        pattern = f"{full_regex}|{partial_comment_regex}"
        
        return re.compile(pattern, re.DOTALL | re.MULTILINE)
        
    @staticmethod
    def keywords() -> list:
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.ruby
