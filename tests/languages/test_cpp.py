from PyReprism.languages.cpp import CPP
import pytest

class TestJava:
    @staticmethod
    def test_instance_creation():
        try:
            instance = CPP()
        except Exception as e:
            pytest.fail(f"Instance creation failed with exception: {e}")
        assert isinstance(instance, CPP)
    @staticmethod
    def test_extension():
        ext = CPP.file_extension()
        assert ext == ".cpp"

    @staticmethod
    def test_remove_comments():
        source_code = '''
int main() {
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
int main() {

int a = 5;
int b = 6;

}
'''

        output = CPP.remove_comments(source_code)
        assert output == expected_output.strip()
        print("Test remove_comments passed!")