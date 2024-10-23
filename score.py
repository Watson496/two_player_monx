from fractions import Fraction
from functools import lru_cache
import math


class Score:
    def __init__(self, m_1: int, n_1: int, m_2: int, n_2: int):
        self.m_1 = m_1
        self.n_1 = n_1
        self.m_2 = m_2
        self.n_2 = n_2

    def key(self):
        return (self.m_1, self.n_1, self.m_2, self.n_2)

    def __hash__(self):
        return hash(self.key())

    def __eq__(self, other):
        return self.key() == other.key()

    def hat_p(self) -> Fraction:
        # Thm.1
        if self.m_1 == 1 and self.n_2 == 1 and self.m_2 == 1 and self.n_2 == 1:
            return Fraction(1, 2)

        # Thm.2
        if self.m_1 == 1 and self.m_2 == 1 and self.n_2 == 1:
            return Fraction(1, self.n_1 + 1)
        if self.m_1 == 1 and self.n_2 == 1 and self.m_2 == 1:
            return Fraction(1, self.n_2 + 1)

        # Thm.3
        if self.m_1 == 1 and self.m_2 == 1:
            return Fraction(1, self.n_1 + self.n_2)

        # Thm.4
        if self.n_1 == 1 and self.m_2 == 1 and self.n_2 == 1:
            return Fraction(self.m_1, self.m_1 + 1)
        if self.m_1 == 1 and self.n_1 == 1 and self.n_2 == 1:
            return Fraction(self.m_2, self.m_2 + 1)

        # Thm.5
        if self.n_1 == 1 and self.n_2 == 1:
            return Fraction(self.m_1 + self.m_2 - 1, self.m_1 + self.m_2)

        # Thm.6
        if self.m_2 == 1 and self.n_2 == 1:
            return Fraction(self.m_1, self.m_1 + self.n_1)
        if self.m_1 == 1 and self.n_1 == 1:
            return Fraction(self.m_2, self.m_2 + self.n_2)

        # Thm.7
        if self.n_1 == 1 and self.m_2 == 1:
            return Fraction(self.m_1, self.m_1 + self.n_2)
        if self.m_1 == 1 and self.n_2 == 1:
            return Fraction(self.m_2, self.m_2 + self.n_1)

        # 一般式
        W_m_1_1 = Score(
            m_1=self.m_1 - 1, n_1=self.n_1, m_2=self.m_2, n_2=self.n_2
        ).W_1()
        W_n_1_1 = Score(
            m_1=self.m_1, n_1=self.n_1 - 1, m_2=self.m_2, n_2=self.n_2
        ).W_1()
        W_m_2_1 = Score(
            m_1=self.m_1, n_1=self.n_1, m_2=self.m_2 - 1, n_2=self.n_2
        ).W_1()
        W_n_2_1 = Score(
            m_1=self.m_1, n_1=self.n_1, m_2=self.m_2, n_2=self.n_2 - 1
        ).W_1()

        # hat_p*W_m_1_1 + (1-hat_p)*W_n_1_1 == hat_p*W_m_2_1 + (1-hat_p)*W_n_2_1
        # hat_p*(W_m_1_1 - W_m_2_1) == (1-hat_p)*(W_n_2_1 - W_n_1_1)
        # 1/hat_p == 1 - (W_m_1_1 - W_m_2_1)/(W_n_1_1 - W_n_2_1)
        # hat_p = (W_n_2_1 - W_n_1_1)/(W_m_1_1 - W_n_1_1 - W_m_2_1 + W_n_2_1)

        return Fraction(W_n_2_1 - W_n_1_1, W_m_1_1 - W_n_1_1 - W_m_2_1 + W_n_2_1)

    @lru_cache(maxsize=None)
    def W_1(self) -> Fraction:
        if self.m_1 == 0 or self.n_2 == 0:
            return Fraction(1)
        if self.m_2 == 0 or self.n_1 == 0:
            return Fraction(0)

        # Thm.1
        if self.m_1 == 1 and self.n_2 == 1 and self.m_2 == 1 and self.n_2 == 1:
            return Fraction(1, 2)

        # Thm.2
        if self.m_1 == 1 and self.m_2 == 1 and self.n_2 == 1:
            return Fraction(self.n_1, self.n_1 + 1)
        if self.m_1 == 1 and self.n_2 == 1 and self.m_2 == 1:
            return Fraction(1, self.n_2 + 1)

        # Thm.3
        if self.m_1 == 1 and self.m_2 == 1:
            return Fraction(self.n_1, self.n_1 + self.n_2)

        # Thm.4
        if self.n_1 == 1 and self.m_2 == 1 and self.n_2 == 1:
            return Fraction(1, self.m_1 + 1)
        if self.m_1 == 1 and self.n_1 == 1 and self.n_2 == 1:
            return Fraction(self.m_2, self.m_2 + 1)

        # Thm.5
        if self.n_1 == 1 and self.n_2 == 1:
            return Fraction(self.m_2, self.m_1 + self.m_2)

        # Thm.6
        if self.m_2 == 1 and self.n_2 == 1:
            return Fraction(self.n_1, self.m_1 + self.n_1)
        if self.m_1 == 1 and self.n_1 == 1:
            return Fraction(self.m_2, self.m_2 + self.n_2)

        # Thm.7
        if self.n_1 == 1 and self.m_2 == 1:
            return Fraction(1, math.comb(self.m_1 + self.n_2, self.m_1))
        if self.m_1 == 1 and self.n_2 == 1:
            return 1 - Fraction(1, math.comb(self.m_2 + self.n_1, self.m_2))

        # 一般式
        W_m_1_1 = Score(
            m_1=self.m_1 - 1, n_1=self.n_1, m_2=self.m_2, n_2=self.n_2
        ).W_1()
        W_n_1_1 = Score(
            m_1=self.m_1, n_1=self.n_1 - 1, m_2=self.m_2, n_2=self.n_2
        ).W_1()
        W_m_2_1 = Score(
            m_1=self.m_1, n_1=self.n_1, m_2=self.m_2 - 1, n_2=self.n_2
        ).W_1()
        W_n_2_1 = Score(
            m_1=self.m_1, n_1=self.n_1, m_2=self.m_2, n_2=self.n_2 - 1
        ).W_1()

        return Fraction(
            self.hat_p() * W_m_1_1 + (1 - self.hat_p()) * W_n_1_1, 2
        ) + Fraction(self.hat_p() * W_m_2_1 + (1 - self.hat_p()) * W_n_2_1, 2)

    @lru_cache(maxsize=None)
    def W_2(self) -> Fraction:
        return 1 - self.W_1()

    def summary(self) -> dict:
        return {
            "S": f"{{({self.m_1}, {self.n_1}), ({self.m_2}, {self.n_2})}}",
            "m_1": self.m_1,
            "n_1": self.n_1,
            "m_2": self.m_2,
            "n_2": self.n_2,
            "hat_p": str(self.hat_p()),
            "W_1": str(self.W_1()),
            "W_2": str(self.W_2()),
        }
