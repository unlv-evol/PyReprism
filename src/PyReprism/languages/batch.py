import re
from PyReprism.utils import extension


class Batch:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.batch
    
    @staticmethod
    def keywords() -> list:
         keyword = 'not|cmdextversion|defined|errorlevel|exist|echo|set'.split('|')
        
         return keyword
    
    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>REM.*?$|::.*?$)|(?P<noncomment>[^:R]*[^\n]*)', re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex():
        pattern = ''
        return pattern
    
    @staticmethod
    def operator_regex():
        pattern = re.compile(r'\^|==|\b(?:equ|neq|lss|leq|gtr|geq)\b|([*\/%+\-&^|]=?|<<=?|>>=?|[!~_=])')
        return pattern
    
    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(Batch.keywords()) + r')\b')
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in Batch.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)


    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(Batch.keywords_regex()), '', source)
    