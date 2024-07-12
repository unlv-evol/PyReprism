import re
from PyReprism.utils import extension

class Kotlin:
    def __init__():
        pass

    @staticmethod
    def comment():

        # JS, SCALA, CPP, Kotlin, gradle
        full_regex = re.compile(r'(?P<comment>//.*?$|[{}]+)|(?P<multilinecomment>/\*.*?\*/)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"]*)', re.DOTALL | re.MULTILINE)
        partial_comment_regex = re.compile(r'(?P<comment>/\*.*?$|^.*?\*/)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"{}]*)', re.DOTALL)

        pattern = f"{full_regex}|{partial_comment_regex}"
        
        return re.compile(pattern, re.DOTALL | re.MULTILINE)
        
    
    @staticmethod
    def file_extension():
        return extension.kotlin
    
    @staticmethod
    def keywords() -> list:
        pass

    @staticmethod
    def remove_comments(source: str) -> str:
        return re.sub(Kotlin.comment, '', source)

    @staticmethod
    def remove_keywords(source: str):
        keywords = Kotlin.keywords()
        pattern = r'\b(' + '|'.join(keywords) + r')\b'
  
        return re.sub(re.compile(pattern), '', source)