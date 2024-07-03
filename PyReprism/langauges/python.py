import re
from utils import FileExtension

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
    def file_extension():
        return FileExtension.python
    
    @staticmethod
    def keywords():
        pass