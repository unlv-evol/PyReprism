import re
from PyReprism.utils import extension

class MatLab:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.matlab
    
    @staticmethod
    def keywords() -> list:
         keyword = 'break|case|catch|continue|else|elseif|end|for|function|if|inf|NaN|otherwise|parfor|pause|pi|return|switch|try|while'.split('|')
        
         return keyword
    
    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>%\{[\s\S]*?\}%|%.*?$)|(?P<noncomment>[^%]*)', re.MULTILINE
        )
        return pattern
    
    @staticmethod
    def number_regex():
        pattern = re.compile(r'(?:\b\d+\.?\d*|\B\.\d+)(?:[eE][+-]?\d+)?(?:[ij])?|\b[ij]\b', re.IGNORECASE)
        return pattern
    
    @staticmethod
    def operator_regex():
        pattern = re.compile(r"\.?[*^\/\\']|[+\-:@]|[<>=~]=?|&&?|\|\|?")
        return pattern
    
    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(MatLab.keywords()) + r')\b', re.IGNORECASE)
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in MatLab.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)


    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(MatLab.keywords_regex()), '', source)
