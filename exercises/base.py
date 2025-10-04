# exercises/base.py
from abc import ABC, abstractmethod

class BaseProblem(ABC):
    slug = 'base'
    name = 'Base Problem'

    @abstractmethod
    def generate(self, difficulty: int) -> dict:
        """
        Повертає dict з keys:
        - question (str)
        - canonical_answer (str)  # у формі, що перевіряється
        - params (dict)  # для відтворення
        """
        pass

    @abstractmethod
    def check(self, user_input: str, canonical_answer: str, params: dict) -> (bool, str):
        """
        Повертає (is_correct: bool, feedback: str|None)
        """
        pass
