from PyReprism.utils.normalizer import Normalizer


class TestNormalizer:

    @staticmethod
    def test_remove_whitespaces():
        str = "This This"
        expected = "ThisThis"
        data = Normalizer.remove_whitespaces(str)
        assert data == expected
        