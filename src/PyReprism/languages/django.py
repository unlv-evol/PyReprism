import re
from PyReprism.utils import extension


class Django:
    def __init__(self):
        pass

    @staticmethod
    def file_extension() -> str:
        """
        Return the file extension used for Python files.

        :return: The file extension for Python files.
        :rtype: str
        """
        return extension.django

    @staticmethod
    def keywords() -> list:
        """
        Return a list of Python keywords and built-in functions.

        :return: A list of Python keywords and built-in function names.
        :rtype: list
        """
        keyword = 'load|verbatim|widthratio|ssi|firstof|for|url|ifchanged|csrf_token|lorem|ifnotequal|autoescape|now|templatetag|debug|cycle|ifequal|regroup|comment|filter|endfilter|if|spaceless|with|extends|block|include|else|empty|endif|endfor|as|endblock|endautoescape|endverbatim|trans|endtrans|[Tt]rue|[Ff]alse|[Nn]one|in|is|static|macro|endmacro|call|endcall|set|endset|raw|endraw'.split('|')
        return keyword

    @staticmethod
    def functions() -> list:
        """
        Return a list of Python keywords and built-in functions.

        :return: A list of Python keywords and built-in function names.
        :rtype: list
        """
        func = 'abs|add|addslashes|attr|batch|callable|capfirst|capitalize|center|count|cut|d|date|default|default_if_none|defined|dictsort|dictsortreversed|divisibleby|e|equalto|escape|escaped|escapejs|even|filesizeformat|first|float|floatformat|force_escape|forceescape|format|get_digit|groupby|indent|int|iriencode|iterable|join|last|length|length_is|linebreaks|linebreaksbr|linenumbers|list|ljust|lower|make_list|map|mapping|number|odd|phone2numeric|pluralize|pprint|random|reject|rejectattr|removetags|replace|reverse|rjust|round|safe|safeseq|sameas|select|selectattr|sequence|slice|slugify|sort|string|stringformat|striptags|sum|time|timesince|timeuntil|title|trim|truncate|truncatechars|truncatechars_html|truncatewords|truncatewords_html|undefined|unordered_list|upper|urlencode|urlize|urlizetrunc|wordcount|wordwrap|xmlattr|yesno'.split('|')
        return func

    @staticmethod
    def comment_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify different types of comments and non-comment code in Python source files.

        :return: A compiled regex pattern with named groups to match single-line comments, multiline comments, and non-comment code elements.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'(?P<comment>#.*?$)|'r'(?P<multilinecomment1>""".*?""")|'r'(?P<multilinecomment2>\'\'\'.*?\'\'\')|'r'(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^#\'"]*)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify numeric literals in Python code.

        :return: A compiled regex pattern to match Python numeric literals, including integers, floats, and complex numbers.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'')
        return pattern

    @staticmethod
    def operator_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Python operators.

        :return: Regex pattern to match various Python operators and logical keywords.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'')
        return pattern

    @staticmethod
    def keywords_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Python keywords.

        :return: A compiled regex pattern to match Python keywords.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(' + '|'.join(Django.keywords()) + r')\b')

    @staticmethod
    def boolean_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Python boolean literals.

        :return: A compiled regex pattern to match Python boolean literals and `None`.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(?:True|False|None)\b')

    @staticmethod
    def delimiters_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify Python delimiters.

        :return: A compiled regex pattern to match Python delimiters.
        :rtype: re.Pattern
        """
        return re.compile(r'[()\[\]{}.,:;@]')

    @staticmethod
    def remove_comments(source_code: str) -> str:
        """
        Remove comments from the provided Python source code string.

        :param str source_code: The Python source code from which to remove comments.
        :return: The source code with all comments removed.
        :rtype: str
        """
        return Django.comment_regex().sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()

    @staticmethod
    def remove_keywords(source: str) -> str:
        """
        Remove all Python keywords from the provided source code string.

        :param str source: The source code string from which to remove Python keywords.
        :return: The source code string with all Python keywords removed.
        :rtype: str
        """
        return re.sub(re.compile(Django.keywords_regex()), '', source)
