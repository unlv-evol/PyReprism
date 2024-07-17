import re
from PyReprism.utils import extension


class Dart:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.dart
    
    @staticmethod
    def keywords() -> list:
         keyword = 'abstract|assert|async|await|break|case|catch|class|const|continue|default|deferred|do|dynamic|else|enum|export|external|extends|factory|final|finally|for|get|if|implements|import|in|library|new|null|operator|part|rethrow|return|set|static|super|switch|this|throw|try|typedef|var|void|while|with|yield|sync'.split('|')
        
         return keyword
    
    @staticmethod
    def comment_regex():
        pattern = pattern = re.compile(r'(?P<comment>//.*?$|/\*[\s\S]*?\*/|/\*.*?$|^.*?\*/|///.*?$)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"]*)', re.DOTALL | re.MULTILINE)
        return pattern

    
    @staticmethod
    def number_regex():
        pattern = re.compile(r'\b0x[\da-f]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?')
        return pattern
    
    @staticmethod
    def operator_regex():
        pattern = re.compile(r'\bis!|\b(?:as|is)\b|\+\+|--|&&|\|\||<<=?|>>=?|~(?:\/=?)?|[+\-*\/%&^|=!<>]=?|\?')
        return pattern
    
    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(Dart.keywords()) + r')\b')
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in Dart.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)


    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(Dart.keywords_regex()), '', source)