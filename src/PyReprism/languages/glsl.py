import re
from PyReprism.utils import extension
from .base import BaseLanguage
from .registry import LanguageRegistry


@LanguageRegistry.register
class Glsl(BaseLanguage):
	"""GLSL shader language minimal support.

	Handles C-style single-line and block comments conservatively.
	"""
	@classmethod
	def file_extension(cls) -> str:
		return extension.glsl

	@classmethod
	def keywords(cls) -> list:
		return (
			'attribute|const|uniform|varying|buffer|shared|coherent|volatile|restrict|'
			'readonly|writeonly|layout|centroid|flat|smooth|noperspective|patch|sample|'
			'break|continue|do|for|while|switch|case|default|if|else|in|out|inout|'
			'void|bool|true|false|int|uint|float|double|discard|return|struct|precision|'
			'highp|mediump|lowp|vec2|vec3|vec4|ivec2|ivec3|ivec4|bvec2|bvec3|bvec4|'
			'mat2|mat3|mat4|sampler2D|sampler3D|samplerCube'
		).split('|')

	@classmethod
	def comment_regex(cls):
		# Match // single-line and /* ... */ block comments; capture non-comment otherwise
		return re.compile(r'(?P<comment>//.*?$|/\*[\s\S]*?\*/)|(?P<noncomment>.[^/]*)', re.DOTALL | re.MULTILINE)

	@classmethod
	def remove_comments(cls, source_code: str, isList: bool = False):
		return super().remove_comments(source_code, isList)

