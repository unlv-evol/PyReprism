import re
from PyReprism.utils import extension


class Json:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.json
    
    @staticmethod
    def keywords() -> list:
         keyword = ''.split('|')
         return keyword
    
    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>//.*?$|/\*[\s\S]*?\*/|/\*.*?$|^.*?\*/)|(?P<noncomment>[^/\n]*[^\n]*)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex():
        pattern = re.compile(r'')
        return pattern
    
    @staticmethod
    def operator_regex():
        pattern = re.compile(r'')
        return pattern
    
    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(Json.keywords()) + r')\b')
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in Json.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(Json.keywords_regex()), '', source)
    
