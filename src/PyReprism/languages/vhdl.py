import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Vhdl(BaseLanguage):
	"""VHDL language helper.

	Provides comment removal (``--`` single-line comments and C-style
	block comments when present), a small keyword set, and basic numeric
	and operator regexes for normalization.
	"""

	@classmethod
	def file_extension(cls) -> str:
		"""Return the file extension used for VHDL files.

		:rtype: str
		"""
		return extension.vhdl

	@classmethod
	def keywords(cls) -> list:
		"""Return a conservative list of VHDL keywords.

		:rtype: list
		"""
		return ["library", "use", "entity", "architecture", "begin", "end", "process", "signal", "port"]

	@classmethod
	def comment_regex(cls) -> re.Pattern:
		"""Return a regex capturing VHDL comments and non-comment text.

		VHDL single-line comments start with ``--``. We also include a
		forgiving capture for C-style block comments (``/* ... */``)
		which may appear in mixed sources.

		:rtype: re.Pattern
		"""
		pattern = r"(?P<comment>--.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>'(?:\\.|[^\\'])*'|\"(?:\\.|[^\\\"])*\"|[^-/'\"\n]+)"
		return re.compile(pattern, re.DOTALL | re.MULTILINE)

	@classmethod
	def number_regex(cls) -> re.Pattern:
		"""Return a regex for numeric literals (heuristic).

		:rtype: re.Pattern
		"""
		return re.compile(r'(?:\b\d+\.?\d*|\B\.\d+)(?:[eE][+-]?\d+)?')

	@classmethod
	def remove_comments(cls, source_code: str, isList: bool = False):
		"""Remove comments and return text or fragments list.

		:param source_code: VHDL source text
		:type source_code: str
		:param isList: when True return list of fragments
		:type isList: bool
		:rtype: list[str] or str
		"""
		return super().remove_comments(source_code, isList=isList)

	@classmethod
	def remove_keywords(cls, source: str) -> str:
		"""Remove known VHDL keywords from the provided source.

		:param source: input text
		:type source: str
		:rtype: str
		"""
		return super().remove_keywords(source)

	@classmethod
	def operator_regex(cls) -> re.Pattern:
		"""Return a regex matching VHDL operators and punctuation.

		:rtype: re.Pattern
		"""
		return re.compile(r'[+\-*/=<>:&|]+')

