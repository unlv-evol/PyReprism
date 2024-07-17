import re
from PyReprism.utils import extension


class Arff:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.arff
    
    @staticmethod
    def keywords() -> list:
         keyword = 'attribute|data|end|relation'.split('|')
        
         return keyword
    
    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>%.*?$)|(?P<noncomment>[^%]*)', re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex():
        pattern = re.compile(r'\b\d+(?:\.\d+)?\b')
        return pattern
    
    @staticmethod
    def operator_regex():
        pattern = ''
        return pattern
    
    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(Arff.keywords()) + r')\b')
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in Arff.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)


    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(Arff.keywords_regex()), '', source)
    
