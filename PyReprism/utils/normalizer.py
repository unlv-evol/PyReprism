import re

class Normalizer:

    @staticmethod
    def whitespaces ():
        return re.compile(r'[\t\x0b\x0c\r ]+')
    



