from PyReprism.languages.html import HTML

class TestHTML:
    @staticmethod
    def test_extension():
        ext = HTML.file_extension()
        assert ext == ".html"

    @staticmethod
    def test_remove_comments():
        source_code = '''
<!-- This is a single-line comment -->
<p> This is a paragraph </p>
}
'''
    
        expected_output = '''

<p> This is a paragraph </p>
}
'''

        output = HTML.remove_comments(source_code)
        assert output == expected_output.strip()
        print("Test remove_comments passed!")

    # @staticmethod
    # def test_keywords():
    #     expected_keywords = [
    #         'abstract', 'continue', 'for', 'new', 'switch', 'assert', 'default', 'goto', 'package', 'synchronized',
    #         'boolean', 'do', 'if', 'private', 'this', 'break', 'double', 'implements', 'protected', 'throw', 'byte',
    #         'else', 'import', 'public', 'throws', 'case', 'enum', 'instanceof', 'return', 'transient', 'catch',
    #         'extends', 'int', 'short', 'try', 'char', 'final', 'interface', 'static', 'void', 'class', 'finally',
    #         'long', 'strictfp', 'volatile', 'const', 'float', 'native', 'super', 'while'
    #     ]
    #     result = Java.keywords()
    #     assert result == expected_keywords