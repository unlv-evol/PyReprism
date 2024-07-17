import re
from PyReprism.utils import extension


class Ruby:
    def __init__(self):
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.ruby
    
    @staticmethod
    def keywords() -> list:
         keyword = 'alias|and|BEGIN|begin|break|case|class|def|define_method|defined|do|each|else|elsif|END|end|ensure|false|for|if|in|module|new|next|nil|not|or|protected|private|public|raise|redo|require|rescue|retry|return|self|super|then|throw|true|undef|unless|until|when|while|yield|Array|Bignum|Binding|Class|Continuation|Dir|Exception|FalseClass|File|Stat|Fixnum|Float|Hash|Integer|IO|MatchData|Method|Module|NilClass|Numeric|Object|Proc|Range|Regexp|String|Struct|TMS|Symbol|ThreadGroup|Thread|Time|TrueClass'.split('|')
        
         return keyword
    
    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>#.*?$|=begin[\s\S]*?=end|=begin.*?$|^.*?=end)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^#=\'"]*)', re.DOTALL | re.MULTILINE)
        return pattern
    
    @staticmethod
    def number_regex():
        pattern = ''
        return pattern
    
    @staticmethod
    def operator_regex():
        pattern = ''
        return pattern
    
    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(Ruby.keywords()) + r')\b', re.IGNORECASE)
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in Ruby.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(Ruby.keywords_regex()), '', source)
