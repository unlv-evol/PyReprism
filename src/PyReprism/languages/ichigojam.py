import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class IchigoJam(BaseLanguage):
	"""IchigoJam BASIC-like language helper.

	Provides comment removal (remarks with ``'`` or line comments) and
	conservative regexes to assist normalization.
	"""

	@classmethod
	def file_extension(cls) -> str:
		"""Return the file extension used for IchigoJam files.

		:rtype: str
		"""
		return extension.ichigojam

	@classmethod
	def keywords(cls) -> list:
		"""Return a small list of BASIC-like keywords.

		:rtype: list
		"""
		return ["LET", "PRINT", "GOTO", "IF", "THEN", "FOR", "NEXT"]

	@classmethod
	def comment_regex(cls) -> re.Pattern:
		# Strings are kept whole.
		return re.compile(
			r"(?P<comment>'[^\n]*$|#.*?$)|(?P<noncomment>\"(?:\\.|[^\\\"\n])*\"|.[^'#\"]*)",
			re.DOTALL | re.MULTILINE)

	@classmethod
	def operator_regex(cls) -> re.Pattern:
		return re.compile(r'[+\-*/=<>!&|%]+')

	@classmethod
	def remove_comments(cls, source_code: str, isList: bool = False):
		return super().remove_comments(source_code, isList=isList)

	@classmethod
	def remove_keywords(cls, source: str) -> str:
		return super().remove_keywords(source)

