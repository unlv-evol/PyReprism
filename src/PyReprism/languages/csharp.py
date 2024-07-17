import re
from PyReprism.utils import extension


class CSharp:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.csharp
    
    @staticmethod
    def keywords() -> list:
         keyword = 'abstract|add|alias|as|ascending|async|await|base|bool|break|byte|case|catch|char|checked|class|const|continue|decimal|default|delegate|descending|do|double|dynamic|else|enum|event|explicit|extern|false|finally|fixed|float|for|foreach|from|get|global|goto|group|if|implicit|in|int|interface|internal|into|is|join|let|lock|long|namespace|new|null|object|operator|orderby|out|override|params|partial|private|protected|public|readonly|ref|remove|return|sbyte|sealed|select|set|short|sizeof|stackalloc|static|string|struct|switch|this|throw|true|try|typeof|uint|ulong|unchecked|unsafe|ushort|using|value|var|virtual|void|volatile|where|while|yield|warning|define|elif|endif|endregion|error|if|line|pragma|region|undef'.split('|')
        
         return keyword
    
    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>//.*?$|/\*.*?\*/|/\*.*?$|^.*?\*/|[{}]+)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"{}]*)', re.DOTALL | re.MULTILINE)
        return pattern

    
    @staticmethod
    def number_regex():
        pattern = re.compile(r'\b0x[\da-f]+\b|(?:\b\d+\.?\d*|\B\.\d+)f?')
        return pattern
    
    @staticmethod
    def operator_regex():
        pattern = re.compile(r'(^|[^.])(?:\+[+=]?|-[-=]?|!=?|<<?=?|>>?>?=?|==?|&[&=]?|\|[|=]?|\*=?|\/=?|%=?|\^=?|[?:~])')
        return pattern
    
    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(CSharp.keywords()) + r')\b')
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in CSharp.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)


    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(CSharp.keywords_regex()), '', source)
    
