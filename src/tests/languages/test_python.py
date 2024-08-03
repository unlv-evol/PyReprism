from PyReprism.languages.python import Python
import pytest

class TestPython:
    @staticmethod
    def test_instance_creation():
        try:
            instance = Python()
        except Exception as e:
            pytest.fail(f"Instance creation failed with exception: {e}")
        assert isinstance(instance, Python)
    @staticmethod
    def test_extension():
        ext = Python.file_extension()
        assert ext == ".py"

    @staticmethod
    def test_remove_comments():
        source_code = '''
        # This is a single-line comment
        def greet():
            """ This is a docstring
            that spans multiple lines """
            print("Hello, World!")  # Inline comment
        '''
    
        expected_output = '''
        def greet():
            
            print("Hello, World!")
        '''

        output = Python.remove_comments(source_code)
    
        assert output == expected_output.strip()
        print("Test remove_comments passed!")

    @staticmethod    
    def test_remove_comments_two():
        source_code = """
        # single line comment
        x = 5 + 6
        '''
        multiline
        comment
        '''
        print(x)
        """
    
        expected_output = '''
        x = 5 + 6
        
        print(x)
        '''

        output = Python.remove_comments(source_code)
    
        assert output == expected_output.strip()
        print("Test remove_comments_two passed!")
       