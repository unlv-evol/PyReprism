
"""GLSL shader language minimal support.

Handles C-style single-line and block comments conservatively.
"""

import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Glsl(BaseLanguage):
	@classmethod
	def file_extension(cls) -> str:
		return extension.glsl

	@classmethod
	def keywords(cls) -> list:
		# keep empty for now; can be extended later
		return []

	@classmethod
	def comment_regex(cls):
		# Match // single-line and /* ... */ block comments; capture non-comment otherwise
		return re.compile(r'(?P<comment>//.*?$)|(?P<comment>/\*[\s\S]*?\*/)|(?P<noncomment>[^/\n][^\n]*)', re.DOTALL | re.MULTILINE)

	@classmethod
	def remove_comments(cls, source_code: str, isList: bool = False):
		return super().remove_comments(source_code, isList)

