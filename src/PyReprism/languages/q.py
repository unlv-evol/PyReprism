
import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Q(BaseLanguage):
	"""Minimal stub for q language (kdb+)."""

	@classmethod
	def file_extension(cls) -> str:
		return extension.q

	@classmethod
	def keywords(cls) -> list:
		return []

	@classmethod
	def comment_regex(cls) -> re.Pattern:
		# Conservative comment matcher: supports //, /* */, and # comments
		return re.compile(r'(?P<comment>//.*?$|/\*[\s\S]*?\*/|#.*?$)|(?P<noncomment>'
						  r"'(?:\\.|[^\\'])*'|\"(?:\\.|[^\\\"])*\"|[^/\#\n'\"]+)",
						  re.DOTALL | re.MULTILINE)

