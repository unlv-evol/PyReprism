
"""Minimal Git commit/patch language support.

This class handles simple comment removal for git-related files
(commit messages, patch fragments)."
"""

import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Git(BaseLanguage):
	@classmethod
	def file_extension(cls) -> str:
		return extension.git

	@classmethod
	def keywords(cls) -> list:
		return []

	@classmethod
	def comment_regex(cls):
		# Git commit files often use # for comments; accept ; as well
		return re.compile(r'(?P<comment>^[#;].*?$)|(?P<noncomment>^[^#;\n].*?$)', re.MULTILINE)

	@classmethod
	def remove_comments(cls, source_code: str, isList: bool = False):
		return super().remove_comments(source_code, isList)

