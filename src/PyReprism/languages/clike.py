import re
from PyReprism.utils import extension


class Clike:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.clike
    
    @staticmethod
    def keywords() -> list:
         keyword = 'if|else|while|do|for|return|in|instanceof|function|new|try|throw|catch|finally|null|break|continue|true|false|class|interface|extends|implements|trait|instanceof|new'.split('|')
        
         return keyword
    
    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>//.*?$|/\*.*?\*/|/\*.*?$|^.*?\*/|[{}]+)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"{}]*)', re.DOTALL | re.MULTILINE)
        return pattern

    
    @staticmethod
    def number_regex():
        pattern = re.compile(r'\b0x[\da-f]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?')
        return pattern
    
    @staticmethod
    def operator_regex():
        pattern = re.compile(r'--?|\+\+?|!=?=?|<=?|>=?|==?=?|&&?|\|\|?|\?|\*|\/|~|\^|%')
        return pattern
    
    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(Clike.keywords()) + r')\b')
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in Clike.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)


    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(Clike.keywords_regex()), '', source)