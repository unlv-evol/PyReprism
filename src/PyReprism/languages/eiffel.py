import re
from PyReprism.utils import extension


class Eiffel:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.eiffel
    
    @staticmethod
    def keywords() -> list:
        keyword = 'across|agent|alias|all|and|attached|as|assign|attribute|check|class|convert|create|Current|debug|deferred|detachable|do|else|elseif|end|ensure|expanded|export|external|feature|from|frozen|if|implies|inherit|inspect|invariant|like|local|loop|not|note|obsolete|old|once|or|Precursor|redefine|rename|require|rescue|Result|retry|select|separate|some|then|undefine|until|variant|Void|when|xor|True|False'.split('|')
        return keyword
    
    @staticmethod
    def comment_regex():
       pattern = re.compile(r'(?P<comment>--.*?$|\{[\s\S]*?\}|\{.*?$|^.*?\})|(?P<noncomment>[^-{]*[^\n]*)', re.DOTALL | re.MULTILINE)
       return pattern

    @staticmethod
    def number_regex():
        pattern = re.compile(r'\b0[xcb][\da-f](?:_*[\da-f])*\b|(?:\d(?:_*\d)*)?\.(?:(?:\d(?:_*\d)*)?e[+-]?)?\d(?:_*\d)*|\d(?:_*\d)*\.?')
        return pattern
    
    @staticmethod
    def operator_regex():
        pattern = re.compile(r'\\\\|\|\.\.\||\.\.|\/[~\/=]?|[><]=?|[-+*^=~]')
        return pattern
    
    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(Eiffel.keywords()) + r')\b')
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in Eiffel.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(Eiffel.keywords_regex()), '', source)