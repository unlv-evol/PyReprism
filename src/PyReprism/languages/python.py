import re
from PyReprism.utils import extension

class Python:
    def __init__():
        pass

    @staticmethod
    def comment():
        
        single_line_comment = r'(?P<comment>#.*?$)'
        single_quote_string = r"(?P<noncomment>'(\\.|[^\\'])*')"
        double_quote_string = r'(?P<noncomment>"(\\.|[^\\"])*")'
        non_comment_part = r".[^#'\"]*"
        triple_double_quotes = r'(?P<multilinecomment>""".*?""")'
        triple_single_quotes = r"(?P<multilinecomment>'''.*?''')"
        
        pattern = (
            f"{single_line_comment}|"
            f"{triple_double_quotes}|"
            f"{triple_single_quotes}|"
            f"{single_quote_string}|"
            f"{double_quote_string}|"
            f"{non_comment_part}"
        )
        
        return re.compile(pattern, re.DOTALL | re.MULTILINE)
        
    
    @staticmethod
    def file_extension() -> str:
        return extension.python
    
    @staticmethod
    def keywords() -> list:
        string = ["as","assert","async","await","break","class","continue","def","del","elif","else","except","exec","finally","for","from","global","if","import","in","is","lambda","nonlocal","pass","print","raise","return","try","while","with","yield","__import__","abs","all","any","apply","ascii","basestring","bin","bool","buffer","bytearray","bytes","callable","chr","classmethod","cmp","coerce","compile","complex","delattr","dict","dir","divmod","enumerate","eval","execfile","file","filter","float","format","frozenset","getattr","globals","hasattr","hash","help","hex","id","input","int","intern","isinstance","issubclass","iter","len","list","locals","long","map","max","memoryview","min","next","object","oct","open","ord","pow","property","range","raw_input","reduce","reload","repr","reversed","round","set","setattr","slice","sorted","staticmethod","str","sum","super","tuple","type","unichr","unicode","vars","xrange","zip","True","False","None"]

    @staticmethod
    def remove_comments(source: str) -> str:
        pass

    @staticmethod
    def remove_keywords(source: str):
        keywords = Python.keywords()
        pattern = r'\b(' + '|'.join(keywords) + r')\b'
  
        return re.compile(pattern)