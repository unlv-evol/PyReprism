import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Verilog(BaseLanguage):
	"""Verilog/SystemVerilog language helper.

	Implements conservative comment removal (C-style // and /* */) and
	provides basic regex helpers for numbers and operators suitable for
	normalization tasks.
	"""

	@classmethod
	def file_extension(cls) -> str:
		"""Return the typical Verilog file extension.

		:rtype: str
		"""
		return extension.verilog

	@classmethod
	def keywords(cls) -> list:
		"""Return a conservative list of Verilog/SystemVerilog keywords.

		:rtype: list
		"""
		return [
			"module",
			"endmodule",
			"input",
			"output",
			"wire",
			"reg",
			"always",
			"assign",
			"begin",
			"end",
		]

	@classmethod
	def comment_regex(cls) -> re.Pattern:
		"""Return a regex that captures comments and non-comment fragments.

		Supports single-line ``//`` and C-style block comments ``/* ... */``,
		and returns named groups ``comment`` and ``noncomment`` for use by
		BaseLanguage.remove_comments.

		:rtype: re.Pattern
		"""
		pattern = r"(?P<comment>//.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>'(?:\\.|[^\\'])*'|\"(?:\\.|[^\\\"])*\"|[^/\'\"\n]+)"
		return re.compile(pattern, re.DOTALL | re.MULTILINE)

	@classmethod
	def number_regex(cls) -> re.Pattern:
		"""Return a regex matching numeric literals commonly found in Verilog.

		:rtype: re.Pattern
		"""
		return re.compile(r'\b(?:\d+\'?[duh]?\d*|\d+|\B\.\d+)')

	@classmethod
	def operator_regex(cls) -> re.Pattern:
		"""Simple operator regex used for token splitting.

		:rtype: re.Pattern
		"""
		return re.compile(r'[+\-*/%=<>!&|:^~]+')

	@classmethod
	def remove_comments(cls, source_code: str, isList: bool = False):
		"""Strip comments and return joined text or list of fragments.

		:param source_code: Verilog source text
		:type source_code: str
		:param isList: if True return list of non-comment fragments
		:type isList: bool
		:rtype: list[str] or str
		"""
		return super().remove_comments(source_code, isList=isList)

	@classmethod
	def remove_keywords(cls, source: str) -> str:
		"""Remove known Verilog keywords using BaseLanguage helper.

		:param source: input text
		:type source: str
		:rtype: str
		"""
		return super().remove_keywords(source)

