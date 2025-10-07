import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Tcl(BaseLanguage):
	"""Tcl language helper.

	Provides comment removal for Tcl (``#`` single-line) and basic
	token regexes.
	"""

	@classmethod
	def file_extension(cls) -> str:
		return extension.tcl

	@classmethod
	def keywords(cls) -> list:
		return ["proc", "set", "if", "else", "foreach", "while", "return"]

	@classmethod
	def comment_regex(cls) -> re.Pattern:
		pattern = re.compile(r'(?P<comment>#.*?$)|(?P<noncomment>[^#\n]+)', re.MULTILINE)
		return pattern

	@classmethod
	def operator_regex(cls) -> re.Pattern:
		return re.compile(r'[+\-*/=<>!&|%:]+')

	@classmethod
	def remove_comments(cls, source_code: str, isList: bool = False):
		return super().remove_comments(source_code, isList=isList)

	@classmethod
	def remove_keywords(cls, source: str) -> str:
		return super().remove_keywords(source)

