from PyReprism.languages.actionscript import ActionScript
import pytest

class TestActionScript:
    @staticmethod
    def test_instance_creation():
        try:
            instance = ActionScript()
        except Exception as e:
            pytest.fail(f"Instance creation failed with exception: {e}")
        assert isinstance(instance, ActionScript)

    @staticmethod
    def test_extension():
        ext = ActionScript.file_extension()
        assert ext == ".as"

    @staticmethod
    def test_remove_comments():
        source_code = '''
private function sayHello():void {
// This function prints "Hello, World!" to the console
trace("Hello, World!"); // Output: Hello, World!
/* This is 
a multiline comment
*/
}
'''
        expected_output = '''
private function sayHello():void {

trace("Hello, World!"); 

}

'''
        output = ActionScript.remove_comments(source_code)
    
        assert output == expected_output.strip()
        print("Test remove_comments passed!")
