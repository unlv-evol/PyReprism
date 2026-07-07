import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Haxe(BaseLanguage):
	"""Haxe language helper.

	Provides conservative comment removal and basic token regexes used by
	normalization utilities.
	"""

	@classmethod
	def file_extension(cls) -> str:
		"""Return the file extension for Haxe source files.

		:rtype: str
		"""
		return extension.haxe

	@classmethod
	def keywords(cls) -> list:
		"""Return a conservative list of Haxe keywords.

		:rtype: list
		"""
		return ["class", "extends", "implements", "var", "function", "if", "else", "return", "package", "import", "new", "static"]

	@classmethod
	def comment_regex(cls) -> re.Pattern:
		"""Return a regex capturing Haxe comments and non-comment fragments.

		Supports C-style block comments and line comments starting with ``//``.
		:rtype: re.Pattern
		"""
		pattern = r"(?P<comment>//.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>'(?:\\.|[^\\'])*'|\"(?:\\.|[^\\\"])*\"|[^/\'\"\n]+)"
		return re.compile(pattern, re.DOTALL | re.MULTILINE)

	@classmethod
	def operator_regex(cls) -> re.Pattern:
		"""Return an operator regex for Haxe tokenization.

		:rtype: re.Pattern
		"""
		return re.compile(r'[+\-*/%=<>!&|:^~]+')

	@classmethod
	def remove_comments(cls, source_code: str, isList: bool = False):
		return super().remove_comments(source_code, isList=isList)

	@classmethod
	def remove_keywords(cls, source: str) -> str:
		return super().remove_keywords(source)

