import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Django(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        return extension.django

    @classmethod
    def keywords(cls) -> list:
        keyword = 'load|verbatim|widthratio|ssi|firstof|for|url|ifchanged|csrf_token|lorem|ifnotequal|autoescape|now|templatetag|debug|cycle|ifequal|regroup|comment|filter|endfilter|if|spaceless|with|extends|block|include|else|empty|endif|endfor|as|endblock|endautoescape|endverbatim|trans|endtrans|[Tt]rue|[Ff]alse|[Nn]one|in|is|static|macro|endmacro|call|endcall|set|endset|raw|endraw'.split('|')
        return keyword

    @classmethod
    def functions(cls) -> list:
        func = 'abs|add|addslashes|attr|batch|callable|capfirst|capitalize|center|count|cut|d|date|default|default_if_none|defined|dictsort|dictsortreversed|divisibleby|e|equalto|escape|escaped|escapejs|even|filesizeformat|first|float|floatformat|force_escape|forceescape|format|get_digit|groupby|indent|int|iriencode|iterable|join|last|length|length_is|linebreaks|linebreaksbr|linenumbers|list|ljust|lower|make_list|map|mapping|number|odd|phone2numeric|pluralize|pprint|random|reject|rejectattr|removetags|replace|reverse|rjust|round|safe|safeseq|sameas|select|selectattr|sequence|slice|slugify|sort|string|stringformat|striptags|sum|time|timesince|timeuntil|title|trim|truncate|truncatechars|truncatechars_html|truncatewords|truncatewords_html|undefined|unordered_list|upper|urlencode|urlize|urlizetrunc|wordcount|wordwrap|xmlattr|yesno'.split('|')
        return func

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        # Match single-line comments and triple-quoted strings as multiline comments.
        pattern = re.compile(
            r"(?P<comment>#.*?$)|(?P<multilinecomment1>\"\"\".*?\"\"\")|(?P<multilinecomment2>'''(.*?)''')|(?P<noncomment>'(\\.|[^\\'])*'|\"(\\.|[^\\\"])*\"|[^#'\"]+)",
            re.DOTALL | re.MULTILINE,
        )
        return pattern

    @classmethod
    def number_regex(cls) -> re.Pattern:
        return re.compile(r'')

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        return re.compile(r'')

    @classmethod
    def keywords_regex(cls) -> re.Pattern:
        return re.compile(r"\b(" + "|".join(cls.keywords()) + r")\b")

    @classmethod
    def boolean_regex(cls) -> re.Pattern:
        return re.compile(r'\b(?:True|False|None)\b')

    @classmethod
    def delimiters_regex(cls) -> re.Pattern:
        return re.compile(r'[()\[\]{}.,:;@]')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        # Preserve original scalar behavior (return stripped string); support
        # the list form via BaseLanguage for signature consistency.
        if isList:
            return super().remove_comments(source_code, isList=True)
        return cls.comment_regex().sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return re.sub(re.compile(cls.keywords_regex()), '', source)
