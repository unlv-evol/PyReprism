import re
from PyReprism.utils import extension


class BrainFuck:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.brainfuck

    @staticmethod
    def keywords() -> list:
        keyword = ["<|>"]
        return keyword

    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>[^><+\-.,[\]]+)|(?P<noncomment>[><+\-.,[\]])')
        return pattern

    @staticmethod
    def number_regex():
        pattern = ''
        return pattern

    @staticmethod
    def operator_regex():
        pattern = re.compile(r'[.,]')
        return pattern

    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(BrainFuck.keywords()) + r')\b')

    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        """
        Remove comments from the provided Brainfuck source code string.

        :param str source_code: The Brainfuck source code from which to remove comments.
        :param bool isList: (Optional) A flag indicating if the input is a list of source code lines. This parameter is not used in the function logic.
        :return: The source code with all comments removed.
        :rtype: str
        """
        return BrainFuck.comment_regex().sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()

        result = []
        for match in BrainFuck.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(BrainFuck.keywords_regex()), '', source)
