import math
from typing import Self

from .abstract import EWM as __EWM


class AverageEWM(__EWM):
    mean: float | None

    def reset(self: Self):
        super().reset()

        self.mean = None

    def update(self: Self, value: float):
        if self.mean is None:
            self.mean = value
        else:
            self.mean *= 1 - self.alpha
            self.mean += self.alpha * value
        super().update(value)

    def compute(self: Self) -> float:
        if self.mean is None:
            raise ValueError(f"{self.__name__} cache is empty.")
        else:
            return self.mean


class VarianceEWM(AverageEWM):
    variance: float | None

    def reset(self: Self):
        super().reset()

        self.variance = None

    def update(self: Self, value: float):
        if self.variance is None or self.mean is None:
            self.variance = 0.0
        else:
            self.variance += self.alpha * (value - self.mean) ** 2
            self.variance *= 1 - self.alpha
        super().update(value)

    def compute(self: Self) -> float:
        if self.variance is None:
            raise ValueError(f"{self.__name__} cache is empty.")
        else:
            return self.variance


class SampleVarianceEWM(VarianceEWM):
    correction: float | None

    def reset(self: Self):
        super().reset()

        self.correction = None

    def update(self: Self, value: float):
        if self.correction is None:
            self.correction = 0.0
        else:
            self.correction *= (1 - self.alpha) ** 2
            self.correction += 2 * self.alpha * (1 - self.alpha)
        super().update(value)

    def compute(self: Self) -> float:
        if self.correction is None or self.variance is None:
            raise ValueError(f"{self.__name__} cache is empty.")
        else:
            try:
                return self.variance / self.correction
            except ZeroDivisionError:
                return float("nan")


class SharpeEWM(VarianceEWM):
    def compute(self: Self) -> float:
        if self.mean is None or self.variance is None:
            raise ValueError(f"{self.__name__} cache is empty.")
        else:
            try:
                return self.mean / math.sqrt(self.variance)
            except ZeroDivisionError:
                return float("nan")


class SampleSharpeEWM(SampleVarianceEWM):
    def compute(self: Self) -> float:
        if self.mean is None or self.variance is None or self.correction is None:
            raise ValueError(f"{self.__name__} cache is empty.")
        else:
            try:
                return self.mean / math.sqrt(self.variance / self.correction)
            except ZeroDivisionError:
                return float("nan")
