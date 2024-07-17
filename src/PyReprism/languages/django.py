import re
from PyReprism.utils import extension


class Django:
    def __init__():
        pass

    @staticmethod
    def file_extension() -> str:
        return extension.django
    
    @staticmethod
    def keywords() -> list:
         keyword = 'load|verbatim|widthratio|ssi|firstof|for|url|ifchanged|csrf_token|lorem|ifnotequal|autoescape|now|templatetag|debug|cycle|ifequal|regroup|comment|filter|endfilter|if|spaceless|with|extends|block|include|else|empty|endif|endfor|as|endblock|endautoescape|endverbatim|trans|endtrans|[Tt]rue|[Ff]alse|[Nn]one|in|is|static|macro|endmacro|call|endcall|set|endset|raw|endraw'.split('|')
         return keyword
    
    @staticmethod
    def functions() -> list:
        func = 'abs|add|addslashes|attr|batch|callable|capfirst|capitalize|center|count|cut|d|date|default|default_if_none|defined|dictsort|dictsortreversed|divisibleby|e|equalto|escape|escaped|escapejs|even|filesizeformat|first|float|floatformat|force_escape|forceescape|format|get_digit|groupby|indent|int|iriencode|iterable|join|last|length|length_is|linebreaks|linebreaksbr|linenumbers|list|ljust|lower|make_list|map|mapping|number|odd|phone2numeric|pluralize|pprint|random|reject|rejectattr|removetags|replace|reverse|rjust|round|safe|safeseq|sameas|select|selectattr|sequence|slice|slugify|sort|string|stringformat|striptags|sum|time|timesince|timeuntil|title|trim|truncate|truncatechars|truncatechars_html|truncatewords|truncatewords_html|undefined|unordered_list|upper|urlencode|urlize|urlizetrunc|wordcount|wordwrap|xmlattr|yesno'.split('|')
        return func
    
    @staticmethod
    def comment_regex():
        pattern = re.compile(r'(?P<comment>\{#.*?#\})|(?P<noncomment>[^{]*[^\n]*)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex():
        pattern = re.compile(r'')
        return pattern
    
    @staticmethod
    def operator_regex():
        pattern = re.compile(r'')
        return pattern
    
    @staticmethod
    def keywords_regex():
        return re.compile(r'\b(' + '|'.join(Django.keywords()) + r')\b')
    
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in Django.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(Django.keywords_regex()), '', source)
    