import re
from PyReprism.utils import extension

from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Wasm(BaseLanguage):
	"""WebAssembly helper (heuristics for .wasm/.wat text).

	Provides comment removal and simple token regexes suitable for the
	textual WebAssembly formats. This is intentionally conservative — the
	implementation focuses on reliably extracting non-comment fragments so
	downstream processors can operate without language-specific parsing.
	"""

	@classmethod
	def file_extension(cls) -> str:
		"""Return the file extension used for WebAssembly files.

		:rtype: str
		"""
		return extension.wasm

	@classmethod
	def keywords(cls) -> list:
		"""Return a short, conservative list of WebAssembly text keywords.

		:rtype: list
		"""
		return [
			"module",
			"func",
			"memory",
			"import",
			"export",
			"global",
			"local",
			"param",
			"result",
			"type",
		]

	@classmethod
	def comment_regex(cls) -> re.Pattern:
		"""Compile and return a regex that captures WebAssembly comments.

		Supports WebAssembly text-style line comments that start with ``;;``
		as well as single-semicolon lines and block comments written as
		``(; ... ;)``. The pattern provides named groups ``comment`` and
		``noncomment`` as required by BaseLanguage helpers.

		:rtype: re.Pattern
		"""
		pattern = r'''(?P<comment>;;.*?$|\(;[\s\S]*?;\)|;.*?$)|(?P<noncomment>'(?:\\.|[^\\'])*'|"(?:\\.|[^\\\"])*"|[^;\(\)'"\n]+)'''
		return re.compile(pattern, re.DOTALL | re.MULTILINE)

	@classmethod
	def number_regex(cls) -> re.Pattern:
		"""Return a regex matching numeric literals (heuristic).

		:rtype: re.Pattern
		"""
		return re.compile(r'(?:\b0x[0-9A-Fa-f]+|\b\d+\.?\d*|\B\.\d+)(?:[eE][+-]?\d+)?')

	@classmethod
	def operator_regex(cls) -> re.Pattern:
		"""Return a simple operator regex suitable for tokenization.

		:rtype: re.Pattern
		"""
		return re.compile(r'[=+\-*/<>!&|%]+')

	@classmethod
	def remove_comments(cls, source_code: str, isList: bool = False):
		"""Remove comments using the BaseLanguage helper.

		:param source_code: the WebAssembly source text
		:type source_code: str
		:param isList: if True return list of non-comment fragments
		:type isList: bool
		:rtype: list[str] or str
		"""
		return super().remove_comments(source_code, isList=isList)

	@classmethod
	def remove_keywords(cls, source: str) -> str:
		"""Remove known keywords from the source using BaseLanguage.

		:param source: input source text
		:type source: str
		:rtype: str
		"""
		return super().remove_keywords(source)

