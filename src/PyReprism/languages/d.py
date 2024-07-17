import re
from PyReprism.utils import extension


class D:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.d
    
    @staticmethod
    def keywords() -> list:
         keyword = 'abstract|alias|align|asm|assert|auto|body|bool|break|byte|case|cast|catch|cdouble|cent|cfloat|char|class|const|continue|creal|dchar|debug|default|delegate|delete|deprecated|do|double|else|enum|export|extern|false|final|finally|float|for|foreach|foreach_reverse|function|goto|idouble|if|ifloat|immutable|import|inout|int|interface|invariant|ireal|lazy|long|macro|mixin|module|new|nothrow|null|out|override|package|pragma|private|protected|public|pure|real|ref|return|scope|shared|short|static|struct|super|switch|synchronized|template|this|throw|true|try|typedef|typeid|typeof|ubyte|ucent|uint|ulong|union|unittest|ushort|version|void|volatile|wchar|while|with|__(?:(?:FILE|MODULE|LINE|FUNCTION|PRETTY_FUNCTION|DATE|EOF|TIME|TIMESTAMP|VENDOR|VERSION)__|gshared|traits|vector|parameters)|string|wstring|dstring|size_t|ptrdiff_t'.split('|')
         return keyword
    
    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>//.*?$|/\*[\s\S]*?\*/|/\*.*?$|^.*?\*/|/\+[\s\S]*?\+/|/\+.*?$|^.*?\+/)|(?P<noncomment>[^/]*[^\n]*)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex():
        pattern = re.compile(r'\b0x\.?[a-f\d_]+(?:(?!\.\.)\.[a-f\d_]*)?(?:p[+-]?[a-f\d_]+)?[ulfi]*')
        return pattern
    
    @staticmethod
    def operator_regex():
        pattern = re.compile(r'\|[|=]?|&[&=]?|\+[+=]?|-[-=]?|\.?\.\.|=[>=]?|!(?:i[ns]\b|<>?=?|>=?|=)?|\bi[ns]\b|(?:<[<>]?|>>?>?|\^\^|[*\/%^~])=?')
        return pattern
    
    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(D.keywords()) + r')\b')
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in D.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(D.keywords_regex()), '', source)
    