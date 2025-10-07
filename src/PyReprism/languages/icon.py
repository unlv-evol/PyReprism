import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Icon(BaseLanguage):
	"""Icon programming language helper.

	Provides a simple set of helpers for comment removal and basic token
	recognition for Icon source files.
	"""

	@classmethod
	def file_extension(cls) -> str:
		"""Return the file extension for Icon files.

		:rtype: str
		"""
		return extension.icon

	@classmethod
	def keywords(cls) -> list:
		"""Return a conservative list of Icon keywords.

		:rtype: list
		"""
		return ["procedure", "if", "then", "else", "every", "return"]

	@classmethod
	def comment_regex(cls) -> re.Pattern:
		"""Return a regex capturing Icon comments and non-comment fragments.

		Icon uses single-line comments starting with "#". Provide a forgiving
		pattern returning named groups 'comment' and 'noncomment'.

		:rtype: re.Pattern
		"""
		pattern = re.compile(r'(?P<comment>#.*?$)|(?P<noncomment>[^#\n]+)', re.MULTILINE)
		return pattern

	@classmethod
	def operator_regex(cls) -> re.Pattern:
		"""Return an operator regex for Icon.

		:rtype: re.Pattern
		"""
		return re.compile(r'[+\-*/=<>!&|%~:^]+')

	@classmethod
	def remove_comments(cls, source_code: str, isList: bool = False):
		return super().remove_comments(source_code, isList=isList)

	@classmethod
	def remove_keywords(cls, source: str) -> str:
		return super().remove_keywords(source)

