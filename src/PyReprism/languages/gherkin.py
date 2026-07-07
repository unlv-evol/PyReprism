
"""Gherkin (Cucumber) language minimal support.

This file provides a conservative implementation suitable for initial
migration to BaseLanguage. It recognizes # comments and basic keywords.
"""

import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Gherkin(BaseLanguage):
	@classmethod
	def file_extension(cls) -> str:
		return extension.gherkin

	@classmethod
	def keywords(cls) -> list:
		return ['Feature', 'Scenario', 'Given', 'When', 'Then', 'And', 'But']

	@classmethod
	def comment_regex(cls):
		return re.compile(r'(?P<comment>^#.*?$)|(?P<noncomment>^[^#\n].*?$)', re.MULTILINE)

	@classmethod
	def remove_comments(cls, source_code: str, isList: bool = False):
		return super().remove_comments(source_code, isList)

