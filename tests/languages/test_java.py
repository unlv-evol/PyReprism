from PyReprism.languages.java import Java
import pytest

class TestJava:
    @staticmethod
    def test_instance_creation():
        try:
            instance = Java()
        except Exception as e:
            pytest.fail(f"Instance creation failed with exception: {e}")
        assert isinstance(instance, Java)

    @staticmethod
    def test_extension():
        ext = Java.file_extension()
        assert ext == ".java"

    @staticmethod
    def test_remove_comments():
        source_code = '''
public class {
// This is a single-line comment
int a = 5;
int b = 6;
/*
This is a multi-line
comment
*/
}
'''
    
        expected_output = '''
public class {

int a = 5;
int b = 6;

}
'''

        output = Java.remove_comments(source_code)
    
        assert output == expected_output.strip()
        print("Test remove_comments passed!")

    @staticmethod
    def test_keywords():
        expected_keywords = [
            'abstract', 'continue', 'for', 'new', 'switch', 'assert', 'default', 'goto', 'package', 'synchronized',
            'boolean', 'do', 'if', 'private', 'this', 'break', 'double', 'implements', 'protected', 'throw', 'byte',
            'else', 'import', 'public', 'throws', 'case', 'enum', 'instanceof', 'return', 'transient', 'catch',
            'extends', 'int', 'short', 'try', 'char', 'final', 'interface', 'static', 'void', 'class', 'finally',
            'long', 'strictfp', 'volatile', 'const', 'float', 'native', 'super', 'while'
        ]
        result = Java.keywords()
        assert result == expected_keywords

       