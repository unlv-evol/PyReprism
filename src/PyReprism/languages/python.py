import re
from PyReprism.utils import extension

class Python:
    def __init__():
        pass

    @staticmethod
    def comment():
        return re.compile(r'(^|[^\\])#.*|\'\'\'[\s\S]*?\'\'\'|\"\"\"[\s\S]*?\"\"\"')
        
    
    @staticmethod
    def file_extension() -> str:
        return extension.python
    
    @staticmethod
    def keywords() -> list:
         keyword = ["as","assert","async","await","break","class","continue","def","del","elif","else","except","exec","finally","for","from","global","if","import","in","is","lambda","nonlocal","pass","print","raise","return","try","while","with","yield","__import__","abs","all","any","apply","ascii","basestring","bin","bool","buffer","bytearray","bytes","callable","chr","classmethod","cmp","coerce","compile","complex","delattr","dict","dir","divmod","enumerate","eval","execfile","file","filter","float","format","frozenset","getattr","globals","hasattr","hash","help","hex","id","input","int","intern","isinstance","issubclass","iter","len","list","locals","long","map","max","memoryview","min","next","object","oct","open","ord","pow","property","range","raw_input","reduce","reload","repr","reversed","round","set","setattr","slice","sorted","staticmethod","str","sum","super","tuple","type","unichr","unicode","vars","xrange","zip","True","False","None"]
        
         return keyword

    @staticmethod
    def remove_comments(source: str) -> str:
        def replacer(match):
            return match.group(1) if match.group(1) else ''
           
        cleaned_code = re.sub(Python.comment(), replacer, source)
        cleaned_code = '\n'.join(line.strip() for line in cleaned_code.splitlines() if line.strip())
        return cleaned_code

    @staticmethod
    def remove_keywords(source: str):
        keywords = Python.keywords()
        pattern = r'\b(' + '|'.join(keywords) + r')\b'
  
        return re.sub(re.compile(pattern), '', source)
    
