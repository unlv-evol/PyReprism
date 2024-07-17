import re
from PyReprism.utils import extension


class Autoit:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.autoit
    
    @staticmethod
    def keywords() -> list:
         keyword = 'Case|Const|Continue(?:Case|Loop)|Default|Dim|Do|Else(?:If)?|End(?:Func|If|Select|Switch|With)|Enum|Exit(?:Loop)?|For|Func|Global|If|In|Local|Next|Null|ReDim|Select|Static|Step|Switch|Then|To|Until|Volatile|WEnd|While|With|True|False'.split('|')
        
         return keyword
    
    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>;.*?$|#cs[\s\S]*?#ce|#cs.*?$|^.*?#ce)|(?P<noncomment>[^;#]*[^\n]*)',re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex():
        pattern = re.compile(r'\b(?:0x[\da-f]+|\d+(?:\.\d+)?(?:e[+-]?\d+)?)\b')
        return pattern
    
    @staticmethod
    def operator_regex():
        pattern = re.compile(r'<[=>]?|[-+*\/=&>]=?|[?^]|\b(?:And|Or|Not)\b')
        return pattern
    
    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(Autoit.keywords()) + r')\b')
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in Autoit.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(Autoit.keywords_regex()), '', source)