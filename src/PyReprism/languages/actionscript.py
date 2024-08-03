import re
from PyReprism.utils import extension


class ActionScript:
    def __init__(self):
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.actionscript

    @staticmethod
    def keywords() -> list:
        keyword = 'as|break|case|catch|class|const|default|delete|do|else|extends|finally|for|function|if|implements|import|in|instanceof|interface|internal|is|native|new|null|package|private|protected|public|return|super|switch|this|throw|try|typeof|use|var|void|while|with|dynamic|each|final|get|include|namespace|native|override|set|static'.split('|')
        return keyword

    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>//.*?$|/\*[^*]*\*+(?:[^/*][^*]*\*+)*?/)|(?P<noncomment>[^/]+)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex():
        pattern = re.compile(r'\b\d+\b')
        return pattern

    @staticmethod
    def operator_regex():
        pattern = re.compile(r'\+\+|--|(?:[+\-*\/%^]|&&?|\|\|?|<<?|>>?>?|[!=]=?)=?|[~?@]')
        return pattern

    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(ActionScript.keywords()) + r')\b')

    @staticmethod
    def remove_comments(source_code: str) -> str:
        return ActionScript.comment_regex().sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()

    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(ActionScript.keywords_regex()), '', source)
