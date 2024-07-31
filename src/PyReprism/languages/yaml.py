import re
from PyReprism.utils import extension


class Yaml:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.yaml

    @staticmethod
    def keywords() -> list:
        keyword = ''.split('|')
        return keyword

    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>#.*?$)|(?P<noncomment>[^#\n]*[^\n]*)', re.MULTILINE)
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
        return re.compile(r'\b(' + '|'.join(Yaml.keywords()) + r')\b')

    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in Yaml.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str):
        pattern = re.sub(re.compile(Yaml.keywords_regex()), '', source)
        return pattern
