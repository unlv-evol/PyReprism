import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Hsts(BaseLanguage):
	"""Helper for HSTS (HTTP Strict Transport Security) policy snippets.

	HSTS snippets are small and mostly header-like; the class provides
	comment removal and token regexes to help normalization utilities.
	"""

	@classmethod
	def file_extension(cls) -> str:
		return extension.hsts

	@classmethod
	def keywords(cls) -> list:
		return ["max-age", "includeSubDomains", "preload"]

	@classmethod
	def comment_regex(cls) -> re.Pattern:
		# Quoted values are kept whole.
		return re.compile(
			r"(?P<comment>#.*?$)|(?P<noncomment>\"(?:\\.|[^\\\"\n])*\"|.[^#\"]*)",
			re.DOTALL | re.MULTILINE)

	@classmethod
	def operator_regex(cls) -> re.Pattern:
		return re.compile(r'[=;:,]+')

	@classmethod
	def remove_comments(cls, source_code: str, isList: bool = False):
		return super().remove_comments(source_code, isList=isList)

	@classmethod
	def remove_keywords(cls, source: str) -> str:
		return super().remove_keywords(source)

