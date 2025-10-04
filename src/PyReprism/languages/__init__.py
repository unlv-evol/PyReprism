__version__ = "0.0.3"

# Minimal lazy loader / registry bridge for language modules.
import importlib
from typing import Any

from .registry import LanguageRegistry


# Pre-declare an __all__ mapping of known language module names (optional).
# Keep it small and let modules register themselves via LanguageRegistry.
__all__ = [
	# common names; modules register on import
	'Python', 'JavaScript', 'CPP', 'C', 'Clike', 'Go', 'MatLab', 'Ruby', 'PHP', 'Bash'
]


def __getattr__(name: str) -> Any:
	"""Lazy-load language module attribute by name.

	Accessing e.g. `PyReprism.languages.Python` will import the submodule
	`PyReprism.languages.python` and return the class object if present.
	"""
	# If already registered, return directly
	cls = LanguageRegistry.get(name)
	if cls:
		return cls

	# Try to import the submodule named by lowercasing the name
	mod_name = name.lower()
	try:
		importlib.import_module(f'.{mod_name}', __name__)
	except ModuleNotFoundError:
		raise AttributeError(f"module {__name__} has no attribute {name}")

	cls = LanguageRegistry.get(name)
	if cls:
		return cls
	raise AttributeError(f"module {__name__} has no attribute {name}")


def get_language_by_extension(ext: str):
	"""Return the first registered language class that reports the given file extension."""
	for name, cls in LanguageRegistry.all().items():
		try:
			if cls.file_extension() == ext:
				return cls
		except Exception:
			continue
	return None

