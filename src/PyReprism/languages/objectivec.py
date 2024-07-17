import re
from PyReprism.utils import extension

class ObjectiveC:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.objectivec
    
    @staticmethod
    def keywords() -> list:
         keyword = 'asm|typeof|inline|auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|in|self|super)\b|(?:@interface|@end|@implementation|@protocol|@class|@public|@protected|@private|@property|@try|@catch|@finally|@throw|@synthesize|@dynamic|@selector'.split('|')
        
         return keyword
    
    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>//.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>[^/]*[^\n]*)',re.MULTILINE)
        return pattern
    
    @staticmethod
    def number_regex():
        pattern = re.compile(r'(?:\b0x[\da-f]+|(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?)[ful]*', re.IGNORECASE)
        return pattern
    
    @staticmethod
    def operator_regex():
        pattern = re.compile(r'-[->]?|\+\+?|!=?|<<?=?|>>?=?|==?|&&?|\|\|?|[~^%?*\/@]')
        return pattern
    
    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(ObjectiveC.keywords()) + r')\b', re.IGNORECASE)
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in ObjectiveC.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(ObjectiveC.keywords_regex()), '', source)
