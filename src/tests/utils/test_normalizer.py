from PyReprism.utils.normalizer import Normalizer


class TestNormalizer:

    @staticmethod
    def test_remove_whitespaces():
        code = """
#This is a single-linecomment
x=1 #This is an end-of-linecomment
y=2 #Another end-of-linecomment
string="Daniel #cs class"
str='''
This is a
multi-linecomment
'''
"""

        expected = """
#Thisisasingle-linecomment
x=1#Thisisanend-of-linecomment
y=2#Anotherend-of-linecomment
string="Daniel#csclass"
str='''
Thisisa
multi-linecomment
'''
"""
        data = Normalizer.remove_whitespaces(code)
        assert data.strip() == expected.strip()
        