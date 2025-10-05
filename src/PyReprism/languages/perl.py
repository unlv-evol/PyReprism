import re
from PyReprism.utils import extension


import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Perl(BaseLanguage):
    """Perl language helper."""

    @classmethod
    def file_extension(cls) -> str:
        return extension.pl

    @classmethod
    def keywords(cls) -> list:
        return sorted([
            'and', 'cmp', 'continue', 'or', 'eq', 'ne', 'xor', 'not', 'm', 's', 'y', 'tr',
            'BEGIN', 'END', 'INIT', 'CHECK', 'DESTROY', 'AUTOLOAD', 'scalar', 'int', 'pack',
            'unpack', 'join', 'split', 'reverse', 'defined', 'undef', 'length', 'substr', 'vec',
            'index', 'rindex', 'abs', 'atan2', 'cos', 'sin', 'exp', 'log', 'sqrt', 'srand', 'rand',
            'time', 'localtime', 'gmtime', 'caller', 'chdir', 'chmod', 'chown', 'chroot', 'closedir',
            'connect', 'dbmclose', 'dbmopen', 'die', 'dump', 'each', 'eof', 'eval', 'exec', 'exists',
            'exit', 'fcntl', 'fileno', 'flock', 'fork', 'format', 'getc', 'getgrent', 'getgrgid',
            'getgrnam', 'gethostbyaddr', 'gethostbyname', 'gethostent', 'getlogin', 'getnetbyaddr',
            'getnetbyname', 'getnetent', 'getpeername', 'getpgrp', 'getppid', 'getpriority',
            'getprotobyname', 'getprotobynumber', 'getprotoent', 'getpwent', 'getpwnam', 'getpwuid',
            'getservbyname', 'getservbyport', 'getservent', 'getsockname', 'getsockopt', 'glob',
            'goto', 'grep', 'hex', 'import', 'ioctl', 'join', 'keys', 'kill', 'lc', 'lcfirst', 'link',
            'listen', 'local', 'localtime', 'lstat', 'map', 'mkdir', 'msgctl', 'msgget', 'msgsnd',
            'my', 'next', 'no', 'oct', 'open', 'opendir', 'ord', 'our', 'pipe', 'pop', 'pos', 'print',
            'printf', 'push', 'q', 'qq', 'qr', 'quotemeta', 'rand', 'read', 'readdir', 'readlink',
            'readpipe', 'recv', 'redo', 'ref', 'rename', 'require', 'reset', 'return', 'rewinddir',
            'rmdir', 'say', 'seek', 'seekdir', 'select', 'semctl', 'semget', 'semop', 'send', 'setgrent',
            'sethostent', 'setnetent', 'setpgrp', 'setpriority', 'setprotoent', 'setpwent', 'setservent',
            'setsockopt', 'shift', 'shmctl', 'shmget', 'shmread', 'shmwrite', 'shutdown', 'sin', 'sleep',
            'socket', 'socketpair', 'sort', 'splice', 'sprintf', 'srand', 'stat', 'state', 'study', 'sub',
            'syscall', 'sysopen', 'sysread', 'sysseek', 'system', 'syswrite', 'tell', 'telldir', 'tie',
            'tied', 'times', 'truncate', 'uc', 'ucfirst', 'umask', 'undef', 'unshift', 'untie', 'use',
            'utime', 'values', 'wait', 'waitpid', 'wantarray', 'write', 'y'
        ])

    @classmethod
    def comment_regex(cls) -> re.Pattern:
        return re.compile(r"(?P<comment>#.*?$)|(?P<noncomment>'(?:\\.|[^\\'])*'|\"(?:\\.|[^\\\"])*\"|[^#\'\"\n]+)", re.DOTALL | re.MULTILINE)

    @classmethod
    def number_regex(cls) -> re.Pattern:
        return re.compile(r'\b0b[01]+\b|\b0x[\da-f]*\.?[\da-fp-]+\b|(?:\b\d+\.?\d*|\B\.\d+)(?:e[+-]?\d+)?')

    @classmethod
    def operator_regex(cls) -> re.Pattern:
        return re.compile(r'(^|[^.])(?:\+[+=]?|-[-=]?|!=?|<<?=?|>>?>?=?|==?|&[&=]?|\|[|=]?|\*=?|\/?=|%=?|\^=?|[?:~])')

    @classmethod
    def keywords_regex(cls) -> re.Pattern:
        return re.compile(r'\b(' + '|'.join(cls.keywords()) + r')\b')

    @classmethod
    def remove_comments(cls, source_code: str, isList: bool = False):
        # Preserve legacy scalar behavior: substitution + strip
        out = re.sub(cls.comment_regex(), lambda m: m.groupdict().get('noncomment') or '', source_code)
        if isList:
            return [out]
        return out.strip()

    @classmethod
    def remove_keywords(cls, source: str) -> str:
        return super().remove_keywords(source)
    @staticmethod
    def remove_comments(source_code: str, isList: bool = False) -> str:
        result = []
        for match in Perl.comment_regex().finditer(source_code):
            if match.group('noncomment'):
                result.append(match.group('noncomment'))
        if isList:
            return result
        return ''.join(result)

    @staticmethod
    def remove_keywords(source: str):
        return re.sub(re.compile(Perl.keywords_regex()), '', source)
