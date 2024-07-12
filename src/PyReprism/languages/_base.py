from abc import ABC, abstractmethod

class Base(ABC):

    @staticmethod
    @abstractmethod
    def comments():
        pass

    @staticmethod
    @abstractmethod
    def remove_comments(source: str):
        pass

    @staticmethod
    @abstractmethod
    def keywords() -> list:
        pass

    @staticmethod
    @abstractmethod
    def remove_keywords():
        pass

    @staticmethod
    @abstractmethod
    def file_extension() -> str:
        pass


