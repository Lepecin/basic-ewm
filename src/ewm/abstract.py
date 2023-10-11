from typing import Self
from abc import ABC, abstractmethod


class EWM(ABC):
    alpha: float

    def __init__(self: Self, alpha: float):
        assert 0 <= alpha <= 1
        self.alpha = alpha

        self.reset()

    @abstractmethod
    def reset(self: Self):
        pass

    @abstractmethod
    def update(self: Self, value: float):
        pass

    @abstractmethod
    def compute(self: Self) -> float:
        pass

    def ewm(self: Self, data: list[float]) -> list[float]:
        self.reset()
        values: list[float] = []
        for datum in data:
            self.update(datum)
            values.append(self.compute())
        return values
