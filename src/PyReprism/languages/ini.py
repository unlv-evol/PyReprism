import re
from PyReprism.utils import extension


class INI:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.ini
    
    @staticmethod
    def keywords() -> list:
        pass
    
    @staticmethod
    def comment_regex():
        pattern = re.compile(r'^[ \t]*;.*$', re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex():
        pass
    
    @staticmethod
    def operator_regex():
        pass
    
    @staticmethod
    def keywords_regex():
        pass
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        return re.sub(re.compile(INI.keywords_regex()), '', source_code)

    @staticmethod
    def remove_keywords(source: str):
        pass
    
