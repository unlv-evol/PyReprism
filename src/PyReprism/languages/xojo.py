import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Xojo(BaseLanguage):
	"""Xojo (formerly REALbasic) language helper.

	Provides conservative comment handling and a minimal keyword list suitable
	for normalization tasks.
	"""

	@classmethod
	def file_extension(cls) -> str:
		"""Return the file extension used for Xojo/REALbasic files.

		:rtype: str
		"""
		return extension.xojo

	@classmethod
	def keywords(cls) -> list:
		"""Return a conservative list of Xojo keywords.

		:rtype: list
		"""
		return [
			"Sub",
			"Function",
			"Dim",
			"As",
			"If",
			"Then",
			"Else",
			"End",
			"For",
			"While",
			"Return",
			"Module",
		]

	@classmethod
	def comment_regex(cls) -> re.Pattern:
		"""Return a regex capturing Xojo comments and non-comment fragments.

		Xojo supports single-line comments starting with ``'`` or ``//`` and
		block comments using ``/* ... */`` in some contexts. Provide a forgiving
		pattern with named groups 'comment' and 'noncomment'.

		:rtype: re.Pattern
		"""
		pattern = r"(?P<comment>//.*?$|'.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>\"(?:\\.|[^\\\"])*\"|'(?:\\.|[^\\'])*'|[^/\'\"\n]+)"
		return re.compile(pattern, re.DOTALL | re.MULTILINE)

	@classmethod
	def number_regex(cls) -> re.Pattern:
		"""Return a basic number literal regex.

		:rtype: re.Pattern
		"""
		return re.compile(r'(?:\b\d+\.?\d*|\B\.\d+)(?:[eE][+-]?\d+)?')

	@classmethod
	def remove_comments(cls, source_code: str, isList: bool = False):
		"""Remove comments returning text or fragment list.

		:param source_code: source text
		:type source_code: str
		:param isList: when True return list of fragments
		:type isList: bool
		:rtype: list[str] or str
		"""
		return super().remove_comments(source_code, isList=isList)

	@classmethod
	def remove_keywords(cls, source: str) -> str:
		"""Remove known Xojo keywords.

		:param source: input text
		:type source: str
		:rtype: str
		"""
		return super().remove_keywords(source)

