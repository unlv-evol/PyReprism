import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Twig(BaseLanguage):
	"""Twig templating language helper.

	Focuses on comment removal for Twig templates (``{# ... #}``) and
	embedded languages while providing small helpers for keywords and
	token regexes used by normalization routines.
	"""

	@classmethod
	def file_extension(cls) -> str:
		"""Return the file extension for Twig templates.

		:rtype: str
		"""
		return extension.twig

	@classmethod
	def keywords(cls) -> list:
		"""Return a small list of Twig control keywords.

		:rtype: list
		"""
		return ["if", "else", "endif", "for", "endfor", "set", "block", "endblock", "include"]

	@classmethod
	def comment_regex(cls) -> re.Pattern:
		"""Compile a regex capturing Twig comments and non-comment content.

		Twig comments are delimited with ``{# ... #}``. The pattern also
		captures quoted strings and returns a 'noncomment' group for other
		content.

		:rtype: re.Pattern
		"""
		# Capture Twig comments {# ... #}, quoted strings, and treat the
		# remainder as non-comment fragments. Keep the pattern simple to
		# avoid quoting fragility when patches are applied.
		pattern = r"(?P<comment>\{#[\s\S]*?#\})|(?P<noncomment>'(?:\\.|[^\\'])*'|\"(?:\\.|[^\\\"])*\"|[^\{\'\"\n]+)"
		return re.compile(pattern, re.DOTALL | re.MULTILINE)

	@classmethod
	def remove_comments(cls, source_code: str, isList: bool = False):
		"""Remove Twig comments and return text or fragments.

		:param source_code: Twig template text
		:type source_code: str
		:param isList: when True return list of fragments
		:type isList: bool
		:rtype: list[str] or str
		"""
		return super().remove_comments(source_code, isList=isList)

	@classmethod
	def remove_keywords(cls, source: str) -> str:
		"""Remove Twig keywords from the provided source.

		:param source: input text
		:type source: str
		:rtype: str
		"""
		return super().remove_keywords(source)

	@classmethod
	def operator_regex(cls) -> re.Pattern:
		"""Return a regex matching common operators used inside templates.

		:rtype: re.Pattern
		"""
		return re.compile(r'[=+\-*/<>!&|%\?:]+')
