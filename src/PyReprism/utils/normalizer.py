import re


class Normalizer:
    def __init__():
        pass

    @staticmethod
    def whitespaces_regex ():
        return re.compile(r'[\t\x0b\x0c\r ]+')
    
    @staticmethod
    def remove_whitespaces (source: str):
        return re.sub(Normalizer.whitespaces_regex(), '', source)




