import re
from PyReprism.utils import extension


class ForTran:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.fortran
    
    @staticmethod
    def keywords() -> list:
        keyword = 'INTEGER|REAL|DOUBLE|PRECISION|COMPLEX|CHARACTER|LOGICAL|/\b(?:END ?)?(?:BLOCK ?DATA|DO|FILE|FORALL|FUNCTION|IF|INTERFACE|MODULE(?! PROCEDURE)|PROGRAM|SELECT|SUBROUTINE|TYPE|WHERE|ALLOCATABLE|ALLOCATE|BACKSPACE|CALL|CASE|CLOSE|COMMON|CONTAINS|CONTINUE|CYCLE|DATA|DEALLOCATE|DIMENSION|DO|END|EQUIVALENCE|EXIT|EXTERNAL|FORMAT|GO ?TO|IMPLICIT(?: NONE)?|INQUIRE|INTENT|INTRINSIC|MODULE PROCEDURE|NAMELIST|NULLIFY|OPEN|OPTIONAL|PARAMETER|POINTER|PRINT|PRIVATE|PUBLIC|READ|RETURN|REWIND|SAVE|SELECT|STOP|TARGET|WHILE|WRITE|ASS'.split('|')
        return keyword
    
    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>!.*?$)|(?P<noncomment>[^!]*[^\n]*)', re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex():
        pattern = re.compile(r'(?:\b\d+(?:\.\d*)?|\B\.\d+)(?:[ED][+-]?\d+)?(?:_\w+)?')
        return pattern
    
    @staticmethod
    def operator_regex():
        pattern = re.compile(r'\*\*|\/\/|=>|[=\/]=|[<>]=?|::|[+\-*=%]|\.(?:EQ|NE|LT|LE|GT|GE|NOT|AND|OR|EQV|NEQV)\.|\.[A-Z]+\.')
        return pattern
    
    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(ForTran.keywords()) + r')\b')
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in ForTran.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(ForTran.keywords_regex()), '', source)