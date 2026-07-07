"""Registry-wide smoke tests.

These guard every registered language cheaply: each must expose a file
extension and be able to strip comments and keywords without raising. This
prevents regressions such as empty/broken language stubs or classes that fail
to register (which would make them unreachable through the public API).
"""
import pytest

from PyReprism.languages import _load_all_languages
from PyReprism.languages.base import BaseLanguage
from PyReprism.languages.registry import LanguageRegistry

# Import every language module so the registry is fully populated.
_load_all_languages()

ALL_LANGUAGES = sorted(LanguageRegistry.all().items())

SAMPLE = (
    'value = 1 // c-line\n'
    '# hash comment\n'
    '-- dash comment\n'
    '/* block comment */\n'
    "name = 'text'  \"more\"\n"
    '<!-- markup comment -->\n'
    '{* smarty comment *}\n'
)


def test_registry_is_populated():
    assert len(ALL_LANGUAGES) > 100


@pytest.mark.parametrize('name, cls', ALL_LANGUAGES)
class TestEveryLanguage:
    def test_is_base_language_subclass(self, name, cls):
        assert issubclass(cls, BaseLanguage)

    def test_has_file_extension(self, name, cls):
        ext = cls.file_extension()
        assert isinstance(ext, str)
        assert ext != ''

    def test_keywords_is_list(self, name, cls):
        assert isinstance(cls.keywords(), list)

    def test_remove_comments_returns_str(self, name, cls):
        assert isinstance(cls.remove_comments(SAMPLE), str)

    def test_remove_comments_islist_returns_list(self, name, cls):
        assert isinstance(cls.remove_comments(SAMPLE, isList=True), list)

    def test_remove_comments_is_idempotent(self, name, cls):
        once = cls.remove_comments(SAMPLE)
        assert cls.remove_comments(once) == once

    def test_remove_keywords_returns_str(self, name, cls):
        assert isinstance(cls.remove_keywords('if while for return class def end'), str)

    def test_public_api_import(self, name, cls):
        import PyReprism.languages as languages
        # Names that survive a round-trip through lower() are reachable lazily.
        if name.lower() == cls.__module__.rsplit('.', 1)[-1]:
            assert getattr(languages, name) is cls
