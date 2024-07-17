import re
from PyReprism.utils import extension


class CSP:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.csp
    
    @staticmethod
    def keywords() -> list:
         keyword = 'base-uri|form-action|frame-ancestors|plugin-types|referrer|reflected-xss|report-to|report-uri|require-sri-for|sandbox) |(?:block-all-mixed-content|disown-opener|upgrade-insecure-requests)(?: |;)|(?:child|connect|default|font|frame|img|manifest|media|object|script|style|worker)-src'.split('|')
         return keyword
    
    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>--.*?$|/\*[\s\S]*?\*/|/\*.*?$|^.*?\*/)|(?P<noncomment>[^/\-]*[^\n]*)', re.DOTALL | re.MULTILINE)
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
        return re.compile(r'\b(' + '|'.join(CSP.keywords()) + r')\b')
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in CSP.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(CSP.keywords_regex()), '', source)
    