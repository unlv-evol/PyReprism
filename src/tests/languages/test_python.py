from PyReprism.languages.python import Python

class TestPython:
    @staticmethod
    def test_extension():
        ext = Python.file_extension()
        assert(ext) == ".py"

    @staticmethod
    def test_remove_comments():
        source_code = """
            # This is a single-line comment
            x = 1  # This is an end-of-line comment
            y = 2  # Another end-of-line comment

            '''
            This is a
            multi-line comment
            '''

            """
        expected_cleaned_code = """x = 1\ny = 2"""
                
        cleaned_code = Python.remove_comments(source_code)
                
        assert cleaned_code == expected_cleaned_code
       