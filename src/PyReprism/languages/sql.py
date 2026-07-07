import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class SQL(BaseLanguage):
    """
    SQL language support approximating the Prism.js SQL grammar:
      - C/line comments: /* */ , -- , // , #
      - Variables: @name, @'quoted', @"quoted", @`quoted`
      - Strings: single/double with escapes and doubled quotes
      - Functions (followed by '(')
      - Extensive keyword list (case-insensitive)
      - Booleans/NULL, numbers, operators, punctuation
    """

    # ---------------------------
    # Meta
    # ---------------------------
    @classmethod
    def file_extension(cls) -> str:
        return extension.sql

    # ---------------------------
    # Keyword / Function sets
    # ---------------------------
    @classmethod
    def functions(cls) -> list:
        # Prism "function" group (only highlighted when followed by '(')
        return "AVG|COUNT|FIRST|FORMAT|LAST|LCASE|LEN|MAX|MID|MIN|MOD|NOW|ROUND|SUM|UCASE".split("|")

    @classmethod
    def keywords(cls) -> list:
        """
        Return a list of SQL keywords.

        :rtype: list[str]
        """
        # Copied/normalized from the Prism keyword list
        kw = (
            "ACTION|ADD|AFTER|ALGORITHM|ALL|ALTER|ANALYZE|ANY|APPLY|AS|ASC|AUTHORIZATION|AUTO_INCREMENT|"
            "BACKUP|BDB|BEGIN|BERKELEYDB|BIGINT|BINARY|BIT|BLOB|BOOL|BOOLEAN|BREAK|BROWSE|BTREE|BULK|BY|"
            "CALL|CASCADE|CASCADED|CASE|CHAIN|CHAR|CHARACTER|CHARSET|CHECK|CHECKPOINT|CLOSE|CLUSTERED|"
            "COALESCE|COLLATE|COLUMN|COLUMNS|COMMENT|COMMIT|COMMITTED|COMPUTE|CONNECT|CONSISTENT|"
            "CONSTRAINT|CONTAINS|CONTAINSTABLE|CONTINUE|CONVERT|CREATE|CROSS|CURRENT|CURRENT_DATE|"
            "CURRENT_TIME|CURRENT_TIMESTAMP|CURRENT_USER|CURSOR|CYCLE|DATA|DATABASE|DATABASES|DATETIME|"
            "DAY|DBCC|DEALLOCATE|DEC|DECIMAL|DECLARE|DEFAULT|DEFINER|DELAYED|DELETE|DELIMITER|DELIMITERS|"
            "DENY|DESC|DESCRIBE|DETERMINISTIC|DISABLE|DISCARD|DISK|DISTINCT|DISTINCTROW|DISTRIBUTED|DO|"
            "DOUBLE|DROP|DUMMY|DUMP|DUMPFILE|DUPLICATE|ELSE|ELSEIF|ENABLE|ENCLOSED|END|ENGINE|ENUM|ERRLVL|"
            "ERRORS|ESCAPE|ESCAPED|EXCEPT|EXEC|EXECUTE|EXISTS|EXIT|EXPLAIN|EXTENDED|FETCH|FIELDS|FILE|"
            "FILLFACTOR|FIRST|FIXED|FLOAT|FOLLOWING|FOR|FOR EACH ROW|FORCE|FOREIGN|FREETEXT|FREETEXTTABLE|"
            "FROM|FULL|FUNCTION|GEOMETRY|GEOMETRYCOLLECTION|GLOBAL|GOTO|GRANT|GROUP|HANDLER|HASH|HAVING|"
            "HOLDLOCK|HOUR|IDENTITY|IDENTITY_INSERT|IDENTITYCOL|IF|IGNORE|IMPORT|INDEX|INFILE|INNER|INNODB|"
            "INOUT|INSERT|INT|INTEGER|INTERSECT|INTERVAL|INTO|INVOKER|ISOLATION|ITERATE|JOIN|KEY|KEYS|KILL|"
            "LANGUAGE|LAST|LEAVE|LEFT|LEVEL|LIMIT|LINENO|LINES|LINESTRING|LOAD|LOCAL|LOCK|LONGBLOB|LONGTEXT|"
            "LOOP|MATCH|MATCHED|MEDIUMBLOB|MEDIUMINT|MEDIUMTEXT|MERGE|MIDDLEINT|MINUTE|MODE|MODIFIES|MODIFY|"
            "MONTH|MULTILINESTRING|MULTIPOINT|MULTIPOLYGON|NATIONAL|NATURAL|NCHAR|NEXT|NO|NONCLUSTERED|NULLIF|"
            "NUMERIC|OF|OFF|OFFSET|OFFSETS|ON|OPEN|OPENDATASOURCE|OPENQUERY|OPENROWSET|OPTIMIZE|OPTION|"
            "OPTIONALLY|ORDER|OUT|OUTER|OUTFILE|OVER|PARTIAL|PARTITION|PERCENT|PIVOT|PLAN|POINT|POLYGON|"
            "PRECEDING|PRECISION|PREPARE|PREV|PRIMARY|PRINT|PRIVILEGES|PROC|PROCEDURE|PUBLIC|PURGE|QUICK|"
            "RAISERROR|READ|READS|REAL|RECONFIGURE|REFERENCES|RELEASE|RENAME|REPEAT|REPEATABLE|REPLACE|"
            "REPLICATION|REQUIRE|RESIGNAL|RESTORE|RESTRICT|RETURN|RETURNS|REVOKE|RIGHT|ROLLBACK|ROUTINE|ROW|"
            "ROWCOUNT|ROWGUIDCOL|ROWS|RTREE|RULE|SAVE|SAVEPOINT|SCHEMA|SECOND|SELECT|SERIAL|SERIALIZABLE|"
            "SESSION|SESSION_USER|SET|SETUSER|SHARE|SHOW|SHUTDOWN|SIMPLE|SMALLINT|SNAPSHOT|SOME|SONAME|SQL|"
            "START|STARTING|STATISTICS|STATUS|STRIPED|SYSTEM_USER|TABLE|TABLES|TABLESPACE|TEMP|TEMPORARY|"
            "TEMPTABLE|TERMINATED|TEXT|TEXTSIZE|THEN|TIME|TIMESTAMP|TINYBLOB|TINYINT|TINYTEXT|TOP|TRAN|"
            "TRANSACTION|TRANSACTIONS|TRIGGER|TRUNCATE|TSEQUAL|TYPE|TYPES|UNBOUNDED|UNCOMMITTED|UNDEFINED|"
            "UNION|UNIQUE|UNLOCK|UNPIVOT|UNSIGNED|UPDATE|UPDATETEXT|USAGE|USE|USER|USING|VALUE|VALUES|"
            "VARBINARY|VARCHAR|VARCHARACTER|VARYING|VIEW|WAITFOR|WARNINGS|WHEN|WHERE|WHILE|WITH|WITHIN|"
            "WITH ROLLUP|WORK|WRITETEXT|YEAR"
        )
        return kw.split("|")

    @classmethod
    def boolean_literals(cls) -> list:
        return ["TRUE", "FALSE", "NULL"]

    # ---------------------------
    # Regexes (compiled)
    # ---------------------------
    @classmethod
    def comment_regex(cls):
        # Accepts /* ... */, --..., //..., #... (line-based)
        return re.compile(
            r"(?P<comment>/\*[\s\S]*?\*/|--.*?$|//.*?$|#.*?$)"
            r"|(?P<noncomment>\"(\\.|\"\"|[^\"\\])*\"|'(\\.|''|[^'\\])*'|`(\\.|[^`\\])*`|.[^/\-#\"]*)",
            re.DOTALL | re.MULTILINE
        )

    @classmethod
    def variable_regex(cls):
        # @'quoted' | @"quoted" | @`quoted` | @name (allows dots and $ per Prism)
        return re.compile(r'@(["\'`])(?:\\.|(?!\1)[^\\])+\1|@[\w.$]+')

    @classmethod
    def string_regex(cls):
        # Single or double quotes; supports escapes and doubled quotes
        return re.compile(r'"(?:\\.|""|[^"\\])*"|\'(?:\\.|\'\'|[^\'\\])*\'', re.DOTALL)

    @classmethod
    def function_regex(cls):
        # Functions only when followed by '('
        return re.compile(r"\b(" + "|".join(cls.functions()) + r")\b(?=\s*\()", re.IGNORECASE)

    @classmethod
    def keywords_regex(cls):
        # Big keyword set (case-insensitive)
        return re.compile(r"\b(" + "|".join(map(re.escape, cls.keywords())) + r")\b", re.IGNORECASE)

    @classmethod
    def boolean_regex(cls):
        return re.compile(r"\b(" + "|".join(cls.boolean_literals()) + r")\b", re.IGNORECASE)

    @classmethod
    def number_regex(cls):
        # Hex, ints, floats, leading dot floats; optional scientific notation
        return re.compile(r"\b0x[\da-fA-F]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:[Ee]-?\d+)?")

    @classmethod
    def operator_regex(cls):
        # Symbol operators + word operators like AND/OR/LIKE/BETWEEN/...
        word_ops = r"\b(?:AND|BETWEEN|IN|LIKE|NOT|OR|IS|DIV|REGEXP|RLIKE|SOUNDS LIKE|XOR)\b"
        sym_ops = r"[-+*/=%^~]|&&?|\|\|?|!=?|<(?:=>?|<|>)?|>[>=]?"
        return re.compile(f"(?:{word_ops})|(?:{sym_ops})", re.IGNORECASE)

    @classmethod
    def punctuation_regex(cls):
        # Matches Prism's punctuation set: ; [ ] ( ) ` , .
        return re.compile(r"[;\[\]\(\)`,.]")

    # ---------------------------
    # Helpers
    # ---------------------------
    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        # Defer to BaseLanguage’s implementation if it expects (comment|noncomment) groups.
        return super().remove_comments(source_code, isList)

    @classmethod
    def remove_keywords(cls, source: str):
        return re.sub(cls.keywords_regex(), "", source)
