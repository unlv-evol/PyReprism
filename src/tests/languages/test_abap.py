from PyReprism.languages.abap import Abap
import pytest

class TestAbap:
    @staticmethod
    def test_instance_creation():
        try:
            instance = Abap()
        except Exception as e:
            pytest.fail(f"Instance creation failed with exception: {e}")
        assert isinstance(instance, Abap)

    @staticmethod
    def test_extension():
        ext = Abap.file_extension()
        assert ext == ".abap"

    @staticmethod
    def test_remove_comments():
        source_code = '''
* This is a full line comment
DATA: lv_value TYPE i.
" This is an inline comment
lv_value = 42. " Inline comment at the end of a line
WRITE: / 'This is not a comment'.
(* This is a multi-line comment
   that spans multiple lines
*)
WRITE: / 'This is also not a comment'.
'''
        expected_output = '''
WRITE: / 'This is also not a comment'.
'''
        output = Abap.remove_comments(source_code)
    
        assert output == expected_output.strip()
        print("Test remove_comments passed!")
