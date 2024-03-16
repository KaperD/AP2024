#!/usr/bin/python3
from typing import Self, Tuple
import os


class APMatrix:
    def __init__(self, data) -> None:
        if len(set([len(row) for row in data])) > 1:
            raise ValueError("Every row must have the same length")
        self.data = data

    def __repr__(self) -> str:
        return f"APMatrix({repr(self.data)})"

    def __str__(self) -> str:
        return os.linesep.join([", ".join([str(value) for value in row]) for row in self.data])

    def __add__(self, other) -> Self:
        self.check_dimensions(other)
        return APMatrix([[a + b for (a, b) in zip(l, r)] for (l, r) in zip(self.data, other.data)])

    def __mul__(self, other) -> Self:
        self.check_dimensions(other)
        return APMatrix([[a * b for (a, b) in zip(l, r)] for (l, r) in zip(self.data, other.data)])

    def __matmul__(self, other) -> Self:
        self.check_matrix_dimensions(other)

        def scalar(row, column):
            res = self.data[row][0] * other.data[0][column]
            for i in range(1, len(self.data[row])):
                res += self.data[row][i] * other.data[i][column]
            return res
        result_rows = self.dimensions()[0]
        result_columns = other.dimensions()[1]
        return APMatrix([[scalar(row, column) for column in range(result_columns)] for row in range(result_rows)])

    def dimensions(self) -> Tuple[int, int]:
        return (len(self.data), len(self.data[0])) if len(self.data) > 0 else (0, 0)

    def check_dimensions(self, other) -> None:
        self_dimensions = self.dimensions()
        other_dimensions = other.dimensions()
        if self_dimensions != other_dimensions:
            raise ValueError(
                f"Dimensions mismatch: {self_dimensions} and {other_dimensions}")

    def check_matrix_dimensions(self, other) -> None:
        self_dimensions = self.dimensions()
        other_dimensions = other.dimensions()
        if self_dimensions[1] != other_dimensions[0]:
            raise ValueError(
                f"Dimensions mismatch for matrix oprtation: {self_dimensions} and {other_dimensions}")


if __name__ == "__main__":
    import numpy as np
    np.random.seed(0)
    a = APMatrix(np.random.randint(0, 10, (10, 10)).tolist())
    b = APMatrix(np.random.randint(0, 10, (10, 10)).tolist())
    sum = a + b
    with open("artifacts/3.1/matrix+.txt", "w") as f:
        f.write(str(sum))
    mul = a * b
    with open("artifacts/3.1/matrix*.txt", "w") as f:
        f.write(str(mul))
    mat_mul = a @ b
    with open("artifacts/3.1/matrix@.txt", "w") as f:
        f.write(str(mat_mul))
