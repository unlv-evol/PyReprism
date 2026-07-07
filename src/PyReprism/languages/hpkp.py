import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Hpkp(BaseLanguage):
	"""Helper for HPKP (HTTP Public Key Pinning) header snippets.

	This is a simple helper focused on comment removal and basic token
	regexes for normalization.
	"""

	@classmethod
	def file_extension(cls) -> str:
		return extension.hpkp

	@classmethod
	def keywords(cls) -> list:
		return ["pin-sha256", "max-age", "includeSubDomains", "report-uri"]

	@classmethod
	def comment_regex(cls) -> re.Pattern:
		pattern = re.compile(r'(?P<comment>#.*?$)|(?P<noncomment>[^#\n]+)', re.MULTILINE)
		return pattern

	@classmethod
	def operator_regex(cls) -> re.Pattern:
		return re.compile(r'[=;:,]+')

	@classmethod
	def remove_comments(cls, source_code: str, isList: bool = False):
		return super().remove_comments(source_code, isList=isList)

	@classmethod
	def remove_keywords(cls, source: str) -> str:
		return super().remove_keywords(source)

