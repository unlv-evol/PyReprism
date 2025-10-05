
import re
try:
	from PyReprism.utils import extension
except Exception:
	from PyRePrism.utils import extension  # fallback

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Qore(BaseLanguage):
	"""Minimal stub for Qore language."""

	@classmethod
	def file_extension(cls) -> str:
		return extension.qore

	@classmethod
	def keywords(cls) -> list:
		return []

	@classmethod
	def comment_regex(cls) -> re.Pattern:
		return re.compile(r'(?P<comment>//.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>[^/\n]+)', re.DOTALL | re.MULTILINE)

