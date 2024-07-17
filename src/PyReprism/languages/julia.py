import re
from PyReprism.utils import extension


class Julia:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.julia
    
    @staticmethod
    def keywords() -> list:
         keyword = 'abstract|baremodule|begin|bitstype|break|catch|ccall|const|continue|do|else|elseif|end|export|finally|for|function|global|if|immutable|import|importall|let|local|macro|module|print|println|quote|return|try|type|typealias|using|while|true|false'.split('|')
        
         return keyword
    
    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>#.*?$|#=[\s\S]*?=#|#=.*?$|^.*?=#)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^#\'"]*)', re.DOTALL | re.MULTILINE)
        return pattern

    
    @staticmethod
    def number_regex():
        pattern = re.compile(r'(?:\b(?=\d)|\B(?=\.))(?:0[box])?(?:[\da-f]+\.?\d*|\.\d+)(?:[efp][+-]?\d+)?j?')
        return pattern
    
    @staticmethod
    def operator_regex():
        pattern = re.compile(r'[-+*^%÷&$\\]=?|\/[\/=]?|!=?=?|\|[=>]?|<(?:<=?|[=:])?|>(?:=|>>?=?)?|==?=?|[~≠≤≥]')
        return pattern
    
    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(Julia.keywords()) + r')\b')
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in Julia.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)


    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(Julia.keywords_regex()), '', source)
    
