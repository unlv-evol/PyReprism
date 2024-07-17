import re
from PyReprism.utils import extension


class AppleScript:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.applescript
    
    @staticmethod
    def keywords() -> list:
         keyword = 'about|above|after|against|apart from|around|aside from|at|back|before|beginning|behind|below|beneath|beside|between|but|by|considering|continue|copy|does|eighth|else|end|equal|error|every|exit|false|fifth|first|for|fourth|from|front|get|given|global|if|ignoring|in|instead of|into|is|it|its|last|local|me|middle|my|ninth|of|on|onto|out of|over|prop|property|put|repeat|return|returning|second|set|seventh|since|sixth|some|tell|tenth|that|the|then|third|through|thru|timeout|times|to|transaction|true|try|until|where|while|whose|with|without|alias|application|boolean|class|constant|date|file|integer|list|number|POSIX file|real|record|reference|RGB color|script|text|centimetres|centimeters|feet|inches|kilometres|kilometers|metres|meters|miles|yards|square feet|square kilometres|square kilometers|square metres|square meters|square miles|square yards|cubic centimetres|cubic centimeters|cubic feet|cubic inches|cubic metres|cubic meters|cubic yards|gallons|litres|liters|quarts|grams|kilograms|ounces|pounds|degrees Celsius|degrees Fahrenheit|degrees Kelvin)'.split('|')
        
         return keyword
    
    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>--.*?$|#.*?$|\(\*[\s\S]*?\*\)|\(\*.*?$|^.*?\*\))|(?P<noncomment>[^#\-\(\*]*)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex():
        pattern = re.compile(r'(?:\b\d+\.?\d*|\B\.\d+)(?:e-?\d+)?\b')
        return pattern
    
    @staticmethod
    def operator_regex():
        pattern = re.compile(r'[&=≠≤≥*+\-\/÷^]|[<>]=?')
        return pattern
    
    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(AppleScript.keywords()) + r')\b')
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in AppleScript.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)


    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(AppleScript.keywords_regex()), '', source)
    