import re
from PyReprism.utils import extension


class Nix:
    def __init__() -> None:
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.nix

    @staticmethod
    def keywords() -> list:
        keyword = 'assert|builtins|else|if|in|inherit|let|null|or|then|with'.split('|')
        return keyword

    @staticmethod
    def comment_regex() -> re.Pattern:
        pattern = re.compile(r'(?P<comment>/\*[\s\S]*?\*/|/\*.*?$|^.*?\*/)|(?P<noncomment>[^/*]*[^\n]*)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex() -> re.Pattern:
        pattern = re.compile(r'')
        return pattern

    @staticmethod
    def operator_regex() -> re.Pattern:
        pattern = re.compile(r'[=!<>]=?|\+\+?|\|\||&&|\/\/|->?|[?@]')
        return pattern

    @staticmethod
    def keywords_regex() -> re.Pattern:
        return re.compile(r'\b(' + '|'.join(Nix.keywords()) + r')\b')
    
    @staticmethod
    def delimiters_regex() -> re.Pattern:
        return re.compile(r'[{}()[\].,:;]')

    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        return Nix.comment_regex().sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()
        result = []
        for match in Nix.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str) -> str:
        return re.sub(re.compile(Nix.keywords_regex()), '', source)
