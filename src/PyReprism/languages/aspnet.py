import re
from PyReprism.utils import extension


class Aspnet:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.aspnet
    
    @staticmethod
    def keywords() -> list:
         keyword = 'Assembly|Control|Implements|Import|Master(?:Type)?|OutputCache|Page|PreviousPageType|Reference|Register'.split('|')
        
         return keyword
    
    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>//.*?$|/\*[\s\S]*?\*/|<!--[\s\S]*?-->|/\*.*?$|^.*?\*/|<!--.*?$|^.*?-->)|(?P<noncomment>[^/<!]*[^\n]*)', re.DOTALL | re.MULTILINE)
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
        return re.compile(r'\b(' + '|'.join(Aspnet.keywords()) + r')\b')
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in Aspnet.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(Aspnet.keywords_regex()), '', source)
    
