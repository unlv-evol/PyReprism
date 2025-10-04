import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Ruby(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.ruby

    @classmethod
    def keywords(cls) -> list:
        return 'alias|and|BEGIN|begin|break|case|class|def|define_method|defined|do|each|else|elsif|END|end|ensure|false|for|if|in|module|new|next|nil|not|or|protected|private|public|raise|redo|require|rescue|retry|return|self|super|then|throw|true|undef|unless|until|when|while|yield|Array|Bignum|Binding|Class|Continuation|Dir|Exception|FalseClass|File|Stat|Fixnum|Float|Hash|Integer|IO|MatchData|Method|Module|NilClass|Numeric|Object|Proc|Range|Regexp|String|Struct|TMS|Symbol|ThreadGroup|Thread|Time|TrueClass'.split('|')

    @classmethod
    def comment_regex(cls):
        return re.compile(r"(?P<comment>#.*?$|=begin[\s\S]*?=end|=begin.*?$|^.*?=end)|(?P<noncomment>'(\\.|[^\\'])*'|\"(\\.|[^\\\"])*\"|.[^#=\'\"]*)", re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls):
        return ''

    @classmethod
    def operator_regex(cls):
        return ''

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False) -> str:
        res = super().remove_comments(source_code, isList=isList)
        if isList:
            return res
        return ''.join(res)

    @classmethod
    def remove_keywords(cls, source: str):
        return re.sub(cls.keywords_regex(), '', source)
