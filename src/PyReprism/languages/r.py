
import re
try:
	from PyReprism.utils import extension
except Exception:
	from PyRePrism.utils import extension  # fallback

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class R(BaseLanguage):
	"""R language helper (minimal)."""

	@classmethod
	def file_extension(cls) -> str:
		return extension.r

	@classmethod
	def keywords(cls) -> list:
		return []

	@classmethod
	def comment_regex(cls) -> re.Pattern:
		# R uses '#' for line comments; support strings as noncomment
		return re.compile(r"(?P<comment>#.*?$)|(?P<noncomment>'(?:\\.|[^\\'])*'|\"(?:\\.|[^\\\"])*\"|[^#'\"\n]+)", re.DOTALL | re.MULTILINE)

