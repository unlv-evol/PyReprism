from PyReprism.languages.python import Python

class TestPython:
    str = ""
    
    @staticmethod
    def test_extension():
        ext = Python.file_extension()
        print(ext)
        assert(ext) == ".py"