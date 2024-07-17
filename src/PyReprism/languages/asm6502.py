import re
from PyReprism.utils import extension


class Asm6502:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.asm6502
    
    @staticmethod
    def keywords() -> list:
         keyword = ''.split('|')
        
         return keyword
    
    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>;.*?$)|(?P<noncomment>[^;]*)', re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex():
        pattern = ''
        return pattern
    
    @staticmethod
    def operator_regex():
        pattern = ''
        return pattern
    
    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(Asm6502.keywords()) + r')\b')
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in Asm6502.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(Asm6502.keywords_regex()), '', source)
    
