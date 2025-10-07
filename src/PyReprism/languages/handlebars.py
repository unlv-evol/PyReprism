import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Handlebars(BaseLanguage):
	"""Handlebars/Mustache templating helper.

	Focuses on removing template comments (``{{!-- ... --}}`` and
	``{{! ... }}``) and providing token regexes useful for normalization.
	"""

	@classmethod
	def file_extension(cls) -> str:
		return extension.handlebars

	@classmethod
	def keywords(cls) -> list:
		return ["if", "else", "each", "with", "unless", "partial"]

	@classmethod
	def comment_regex(cls) -> re.Pattern:
		# Capture Handlebars comments {{!-- ... --}} and {{! ... }} as comments
		pattern = r"(?P<comment>\{\{!--[\s\S]*?--\}\}|\{\{![\s\S]*?\}\})|(?P<noncomment>'(?:\\.|[^\\'])*'|\"(?:\\.|[^\\\"])*\"|[^\{\'\"\n]+)"
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

