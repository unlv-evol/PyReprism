import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Xeora(BaseLanguage):
	"""Xeora language helper (.xeora template files).

	Xeora is a templating language used in some systems; this implementation
	focuses on comment removal and a minimal set of helpers to allow
	normalization and keyword stripping in the rest of the toolchain.
	"""

	@classmethod
	def file_extension(cls) -> str:
		"""Return the file extension for Xeora files.

		:rtype: str
		"""
		return extension.xeora

	@classmethod
	def keywords(cls) -> list:
		"""Return a small set of Xeora directives/keywords.

		:rtype: list
		"""
		return ["if", "else", "end", "for", "foreach", "import", "include"]

	@classmethod
	def comment_regex(cls) -> re.Pattern:
		"""Compile and return a regex capturing Xeora comments.

		Many template languages use ``//`` or ``#`` for single-line comments
		and ``/* ... */`` for block comments. Provide a forgiving pattern that
		captures these forms and returns a 'noncomment' group for text to keep.

		:rtype: re.Pattern
		"""
		pattern = r"(?P<comment>//.*?$|#.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>'(?:\\.|[^\\'])*'|\"(?:\\.|[^\\\"])*\"|[^/#'\"\n]+)"
		return re.compile(pattern, re.DOTALL | re.MULTILINE)

	@classmethod
	def remove_comments(cls, source_code: str, isList: bool = False):
		"""Remove comments and return either joined text or list of fragments.

		:param source_code: the template source
		:type source_code: str
		:param isList: when True return list of fragments
		:type isList: bool
		:rtype: list[str] or str
		"""
		return super().remove_comments(source_code, isList=isList)

	@classmethod
	def remove_keywords(cls, source: str) -> str:
		"""Strip known Xeora keywords using BaseLanguage helper.

		:param source: input text
		:type source: str
		:rtype: str
		"""
		return super().remove_keywords(source)

	@classmethod
	def operator_regex(cls) -> re.Pattern:
		"""Return a regex matching common operators and punctuation in templates.

		This is a conservative pattern intended for token splitting and
		normalization tasks.

		:rtype: re.Pattern
		"""
		return re.compile(r'[=+\-*/<>!&|%^~]+')

