import re
from PyReprism.utils import extension


class Scss:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.scss

    @staticmethod
    def keywords() -> list:
        keyword = ''.split('|')
        return keyword

    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>/\*[\s\S]*?\*/|/\*.*?$|^.*?\*/)|(?P<noncomment>[^/*]*[^\n]*)', re.DOTALL | re.MULTILINE)
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
        return re.compile(r'\b(' + '|'.join(Scss.keywords()) + r')\b')

    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in Scss.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        data = ''.join(result)
        return data

    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(Scss.keywords_regex()), '', source)
