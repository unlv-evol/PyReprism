from PyReprism.languages.python import Python

class TestPython:
    @staticmethod
    def test_extension():
        ext = Python.file_extension()
        assert(ext) == ".py"

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
            """ This is a docstring
            that spans multiple lines """
            print("Hello, World!")
        '''

        output = Python.remove_comments(source_code)
    
        assert output == expected_output.strip()
        print("Test remove_comments passed!")
       