import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Inform7(BaseLanguage):
	"""Inform 7 language helper (authoring language for interactive fiction).

	This implementation is intentionally conservative: it focuses on
	extracting non-comment fragments and provides simple token regexes used
	by normalization utilities.
	"""

	@classmethod
	def file_extension(cls) -> str:
		"""Return the file extension for Inform 7 source files.

		:rtype: str
		"""
		return extension.inform7

	@classmethod
	def keywords(cls) -> list:
		"""Return a small set of Inform 7 control words.

		:rtype: list
		"""
		return ["if", "then", "else", "rule", "when", "instead", "carry"]

	@classmethod
	def comment_regex(cls) -> re.Pattern:
		"""Return a regex capturing comments and non-comment fragments.

		Uses a forgiving set of single-line comment markers (``//``, ``#``,
		``;``) and C-style block comments. Provides named groups
		``comment`` and ``noncomment``.

		:rtype: re.Pattern
		"""
		pattern = r"(?P<comment>//.*?$|#.*?$|;.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>'(?:\\.|[^\\'])*'|\"(?:\\.|[^\\\"])*\"|[^/;#'\"\n]+)"
		return re.compile(pattern, re.DOTALL | re.MULTILINE)

	@classmethod
	def number_regex(cls) -> re.Pattern:
		"""Return a basic numeric literal regex.

		:rtype: re.Pattern
		"""
		return re.compile(r'(?:\b\d+\.?\d*|\B\.\d+)(?:[eE][+-]?\d+)?')

	@classmethod
	def operator_regex(cls) -> re.Pattern:
		"""Return a regex matching common operators.

		:rtype: re.Pattern
		"""
		return re.compile(r'[=+\-*/<>!&|%:^~]+')

	@classmethod
	def remove_comments(cls, source_code: str, isList: bool = False):
		"""Strip comments and return either joined text or list of fragments.

		:param source_code: input text
		:type source_code: str
		:param isList: when True return list of non-comment fragments
		:type isList: bool
		:rtype: list[str] or str
		"""
		return super().remove_comments(source_code, isList=isList)

	@classmethod
	def remove_keywords(cls, source: str) -> str:
		"""Remove known keywords using BaseLanguage helper.

		:param source: input text
		:type source: str
		:rtype: str
		"""
		return super().remove_keywords(source)

