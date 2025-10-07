import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Textile(BaseLanguage):
	"""Textile markup helper.

	Provides comment removal for Textile and simple token helpers for
	normalization.
	"""

	@classmethod
	def file_extension(cls) -> str:
		return extension.textile

	@classmethod
	def keywords(cls) -> list:
		return []

	@classmethod
	def comment_regex(cls) -> re.Pattern:
		# Textile comments are often HTML-style or line-prefixed; support
		# common cases like <!-- ... --> and lines starting with "#"
		pattern = r"(?P<comment><!--[\s\S]*?-->|#.*?$)|(?P<noncomment>'(?:\\.|[^\\'])*'|\"(?:\\.|[^\\\"])*\"|[^<#'\"\n]+)"
		return re.compile(pattern, re.DOTALL | re.MULTILINE)

	@classmethod
	def operator_regex(cls) -> re.Pattern:
		return re.compile(r'[=+\-*/<>!&|%:]+')

	@classmethod
	def remove_comments(cls, source_code: str, isList: bool = False):
		return super().remove_comments(source_code, isList=isList)

	@classmethod
	def remove_keywords(cls, source: str) -> str:
		return super().remove_keywords(source)

