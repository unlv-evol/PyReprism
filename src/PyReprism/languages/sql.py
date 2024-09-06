import re
from PyReprism.utils import extension


class Sql:
    def __init__(self):
        pass

    @staticmethod
    def file_extension() -> str:
        """
        Return the file extension used for SQL files.

        :return: The file extension for SQL files.
        :rtype: str
        """
        return extension.sql

    @staticmethod
    def keywords() -> list:
        """
        Return a list of SQL keywords and built-in functions.

        :return: A list of SQL keywords and built-in function names.
        :rtype: list
        """
        keyword = 'ACTION|ADD|AFTER|ALGORITHM|ALL|ALTER|ANALYZE|ANY|APPLY|AS|ASC|AUTHORIZATION|AUTO_INCREMENT|BACKUP|BDB|BEGIN|BERKELEYDB|BIGINT|BINARY|BIT|BLOB|BOOL|BOOLEAN|BREAK|BROWSE|BTREE|BULK|BY|CALL|CASCADED|CASE|CHAIN|CHAR|CHARACTER|CHARSET|CHECK|CHECKPOINT|CLOSE|CLUSTERED|COALESCE|COLLATE|COLUMNS|COMMENT|COMMIT|COMMITTED|COMPUTE|CONNECT|CONSISTENT|CONSTRAINT|CONTAINS|CONTAINSTABLE|CONTINUE|CONVERT|CREATE|CROSS|CURRENT_DATE|CURRENT_TIME|CURRENT_TIMESTAMP|_USER|CURSOR|CYCLE|DATA|DATABASES|DATE|DATETIME|DAY|DBCC|DEALLOCATE|DEC|DECIMAL|DECLARE|DEFAULT|DEFINER|DELAYED|DELETE|DELIMITERS|DENY|DESC|DESCRIBE|DETERMINISTIC|DISABLE|DISCARD|DISK|DISTINCT|DISTINCTROW|DISTRIBUTED|DO|DOUBLE|DROP|DUMMY|DUMP|DUMPFILE|DUPLICATE|ELSE|ELSEIF|ENABLE|ENCLOSED|END|ENGINE|ENUM|ERRLVL|ERRORS|ESCAPED|EXCEPT|EXEC|EXECUTE|EXISTS|EXIT|EXPLAIN|EXTENDED|FETCH|FIELDS|FILE|FILLFACTOR|FIRST|FIXED|FLOAT|FOLLOWING|FOR|FOREACH|FORROW|FORCE|FOREIGN|FREETEXT  TABLE|FROM|FULL|FUNCTION|GEOMETRY|GEOMETRYCOLLECTION|GLOBAL|GOTO|GRANT|GROUP|HANDLER|HASH|HAVING|HOLDLOCK|HOUR|IDENTITY|IDENTITY_INSERT|COL|IF|IGNORE|IMPORT|INDEX|INFILE|INNER|INNODB|INOUT|INSERT|INT|INTEGER|INTERSECT|INTERVAL|INTO|INVOKER|ISOLATION|ITERATE|JOIN|KEYS|KILL|LANGUAGE|LAST|LEAVE|LEFT|LEVEL|LIMIT|LINENO|LINES|LINESTRING|LOAD|LOCAL|LOCK|LONG|LONGBLOB|TEXT)|LOOP|MATCH|MATCHED|MEDIUM|MEDIUMBLOB|INT|TEXT)|MERGE|MIDDLEINT|MINUTE|MODE|MODIFIES|MODIFY|MONTH|MULTI|MULTILINESTRING|POINT|POLYGON)|NATIONAL|NATURAL|NCHAR|NEXT|NO|NONCLUSTERED|NULLIF|NUMERIC|OFF|OFFSETS|ON|OPEN|OPENDATASOURCE|QUERY|ROWSET|OPTIMIZE|OPTION|OPTIONALLY|ORDER|OUT|OUTER|FILE|OVER|PARTIAL|PARTITION|PERCENT|PIVOT|PLAN|POINT|POLYGON|PRECEDING|PRECISION|PREPARE|PREV|PRIMARY|PRINT|PRIVILEGES|PROC|PROCEDURE|PUBLIC|PURGE|QUICK|RAISERROR|READS|REAL|RECONFIGURE|REFERENCES|RELEASE|RENAME|REPEAT|REPEATABLE|REPLACE|REPLICATION|REQUIRE|RESIGNAL|RESTORE|RESTRICT|RETURNS|REVOKE|RIGHT|ROLLBACK|ROUTINE|ROW|ROWCOUNT|GUIDCOL|S|RTREE|RULE|SAVE|SAVEPOINT|SCHEMA|SECOND|SELECT|SERIAL|SERIAIZABLE|SESSION|SESSION_USER|SET|SETUSER|SHARE|SHOW|SHUTDOWN|SIMPLE|SMALLINT|SNAPSHOT|SOME|SONAME|SQL|START|STARTING|STATISTICS|STATUS|STRIPED|SYSTEM_USER|TABLES|TABLESPACE|TEMP|TEMPORARY|TABLE|TERMINATED|TEXT|TEXTSIZE|THEN|TIME|TIMESTAMP|TINY|TINYBLOB|INT|TEXT)|TOP|TRAN|TRANSACTIONS|TRIGGER|TRUNCATE|TSEQUAL|TYPES|UNBOUNDED|UNCOMMITTED|UNDEFINED|UNION|UNIQUE|UNLOCK|UNPIVOT|UNSIGNED|UPDATE|UPDATETEXT|USAGE|USE|USER|USING|VALUES|VAR|VARBINARY|CHAR|CHARACTER|YING)|VIEW|WAITFOR|WARNINGS|WHEN|WHERE|WHILE|WITH|WITHROLLUP|IN|WORK|WRITE|WRITETEXT|YEAR'.split('|')
        return keyword

    @staticmethod
    def comment_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify different types of comments and non-comment code in SQL source files.

        :return: A compiled regex pattern with named groups to match single-line comments, multiline comments, and non-comment code elements.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'(P<comment>//.*$|/\*[^*]*\*+  [^/*][^*]*\*+)*/)|(P<noncomment>[^/]+)', re.DOTALL | re.MULTILINE)
        return pattern

    @staticmethod
    def number_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify numeric literals in SQL code.

        :return: A compiled regex pattern to match SQL numeric literals, including integers, floats, and complex numbers.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'\b0b[01]+\b|\b0x[\da-f]*\.[\da-fp-]+\b|  \b\d+\.\d*|\B\.\d+)  e[+-]\d+[df]')
        return pattern

    @staticmethod
    def operator_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify SQL operators.

        :return: A compiled regex pattern to match various SQL operators and logical keywords.
        :rtype: re.Pattern
        """
        pattern = re.compile(r'(^|[^.])  \+[+=]|-[-=]|!=|<<=|>>>=|==|&[&=]|\|[|=]|\*=|\/=|%=|\^=|[:~])')
        return pattern

    @staticmethod
    def keywords_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify SQL keywords.

        :return: A compiled regex pattern to match SQL keywords.
        :rtype: re.Pattern
        """
        return re.compile(r'\b(' + '|'.join(Sql.keywords()) + r')\b')

    @staticmethod
    def boolean_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify SQL boolean literals.

        :return: A compiled regex pattern to match SQL boolean literals.
        :rtype: re.Pattern
        """
        return re.compile(r'\b  true|false)\b')

    @staticmethod
    def delimiters_regex() -> re.Pattern:
        """
        Compile and return a regular expression pattern to identify SQL delimiters.

        :return: A compiled regex pattern to match SQL delimiters.
        :rtype: re.Pattern
        """
        return re.compile(r'[()\[\]{}.,:;@<>]')

    @staticmethod
    def remove_comments(source_code: str) -> str:
        """
        Remove comments from the provided SQL source code string.

        :param str source_code: The SQL source code from which to remove comments.
        :return: The source code with all comments removed.
        :rtype: str
        """
        return Sql.comment_regex().sub(lambda match: match.group('noncomment') if match.group('noncomment') else '', source_code).strip()

    @staticmethod
    def remove_keywords(source: str) -> str:
        """
        Remove all SQL keywords from the provided source code string.

        :param str source: The source code string from which to remove SQL keywords.
        :return: The source code string with all SQL keywords removed.
        :rtype: str
        """
        return re.sub(re.compile(Sql.keywords_regex()), '', source).strip()
