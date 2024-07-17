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
         keyword = 'abstract|alignof|as|be|box|break|const|continue|crate|do|else|enum|extern|false|final|fn|for|if|impl|in|let|loop|match|mod|move|mut|offsetof|once|override|priv|pub|pure|ref|return|sizeof|static|self|struct|super|true|trait|type|typeof|unsafe|unsized|use|virtual|where|while|yield'.split('|')
        
         return keyword
    
    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>//.*?$|///.*?$|/\*[\s\S]*?\*/|/\*.*?$|^.*?\*/)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"]*)', re.DOTALL | re.MULTILINE)
        return pattern

    
    @staticmethod
    def number_regex():
        pattern = re.compile(r'\b(?:0x[\dA-Fa-f](?:_?[\dA-Fa-f])*|0o[0-7](?:_?[0-7])*|0b[01](?:_?[01])*|(\d(?:_?\d)*)?\.?\d(?:_?\d)*(?:[Ee][+-]?\d+)?)(?:_?(?:[iu](?:8|16|32|64)?|f32|f64))?\b')
        return pattern
    
    @staticmethod
    def operator_regex():
        pattern = re.compile(r'[-+*\/%!^]=?|=[=>]?|@|&[&=]?|\|[|=]?|<<?=?|>>?=?')
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