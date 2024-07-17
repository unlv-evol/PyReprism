import re
from PyReprism.utils import extension


class CoffeeScript:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.coffeescript
    
    @staticmethod
    def keywords() -> list:
         keyword = 'and|break|by|catch|class|continue|debugger|delete|do|each|else|extend|extends|false|finally|for|if|in|instanceof|is|isnt|let|loop|namespace|new|no|not|null|of|off|on|or|own|return|super|switch|then|this|throw|true|try|typeof|undefined|unless|until|when|while|window|with|yes|yield'.split('|')
         return keyword
    
    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>#.*?$|###.*?###|###.*?$|^.*?###)|(?P<noncomment>[^#]*[^\n]*)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex():
        pattern = re.compile(r' ')
        return pattern
    
    @staticmethod
    def operator_regex():
        pattern = re.compile(r" ")
        return pattern
    
    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(CoffeeScript.keywords()) + r')\b')
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in CoffeeScript.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(CoffeeScript.keywords_regex()), '', source)
    