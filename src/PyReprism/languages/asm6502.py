import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Asm6502(BaseLanguage):
    @classmethod
    def file_extension(cls) -> str:
        """Return the file extension used for 6502 assembly files.

        :rtype: str
        """
        return extension.asm6502

    @classmethod
    def keywords(cls) -> list:
        """Return a list of common 6502 mnemonics.

        The returned list is used to construct a case-insensitive regex when
        matching keywords.

        :rtype: list
        """
        # Common 6502 mnemonics (uppercase preferred); regex will be case-insensitive
        return [
            'ADC','AND','ASL','BCC','BCS','BEQ','BIT','BMI','BNE','BPL','BRK','BVC','BVS',
            'CLC','CLD','CLI','CLV','CMP','CPX','CPY','DEC','DEX','DEY','EOR','INC','INX','INY',
            'JMP','JSR','LDA','LDX','LDY','LSR','NOP','ORA','PHA','PHP','PLA','PLP','ROL','ROR',
            'RTI','RTS','SBC','SEC','SED','SEI','STA','STX','STY','TAX','TAY','TSX','TXA','TXS','TYA',
            'INX','DEX','INY','DEY','INC','DEC'
        ]

    @classmethod
    def comment_regex(cls):
        """Compile and return a regex that captures semicolon comments and non-comment text.

        :rtype: re.Pattern
        """
        return re.compile(r'(?P<comment>;.*?$)|(?P<noncomment>[^;]*)', re.MULTILINE)

    @classmethod
    def number_regex(cls):
        """Return a regex for numeric literals (placeholder).

        :rtype: re.Pattern
        """
        return re.compile(r'')

    @classmethod
    def operator_regex(cls):
        """Return a regex matching operators (placeholder).

        :rtype: re.Pattern
        """
        return re.compile(r'')

    @classmethod
    def keywords_regex(cls):
        """Compile and return the keywords regex (case-insensitive).

        :rtype: re.Pattern
        """
        # Make keyword matching case-insensitive since assembly is often lowercase
        return re.compile(r"\b(" + "|".join(cls.keywords()) + r")\b", re.IGNORECASE)

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        """Remove comments from 6502 assembly source.

        :param source_code: assembly source text
        :type source_code: str
        :param isList: if True return list of non-comment fragments
        :type isList: bool
        :rtype: list[str] or str
        """
        return super().remove_comments(source_code, isList)

    @classmethod
    def remove_keywords(cls, source: str):
        """Remove keywords from the given source string.

        :param source: input source string
        :type source: str
        :rtype: str
        """
        return re.sub(re.compile(cls.keywords_regex()), '', source)
