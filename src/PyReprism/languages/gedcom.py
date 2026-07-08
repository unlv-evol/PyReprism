"""GEDCOM language support for PyRePrism.

This module provides a minimal language class that integrates with the
BaseLanguage + LanguageRegistry architecture. The implementation is
conservative: it recognizes line comments starting with 0 or 1 and
provides empty keyword lists.
"""

import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Gedcom(BaseLanguage):
	@classmethod
	def file_extension(cls) -> str:
		return extension.gedcom

	@classmethod
	def keywords(cls) -> list:
		return []

	@classmethod
	def comment_regex(cls):
		# GEDCOM has numeric-level lines; no formal comment token, but accept lines starting with "0" or "1" as data; treat lines starting with "#" as comment for safety
		return re.compile(r'(?P<comment>^#.*?$)|(?P<noncomment>.[^\n]*|\n)', re.MULTILINE)

	@classmethod
	def remove_comments(cls, source_code: str, isList: bool = False):
		return super().remove_comments(source_code, isList)

