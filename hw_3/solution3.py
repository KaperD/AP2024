#!/usr/bin/python3
import solution1
import solution2


class HashMatrixMixin:
    """
    Возвращаем хэш первого элемента матрицы или 0, если элементов нет.
    """

    def __hash__(self) -> int:
        if len(self.data) == 0 or len(self.data[0]) == 0:
            return 0
        return hash(self.data[0][0])


class CacheMatrixOperationsMixin:
    cache = {}

    def __matmul__(self, other):
        key = (hash(self), hash(other))
        if key in CacheMatrixOperationsMixin.cache:
            return CacheMatrixOperationsMixin.cache[key]
        result = APMatrix(super().__matmul__(other).data)
        CacheMatrixOperationsMixin.cache[key] = result
        return result


class APMatrix(CacheMatrixOperationsMixin, solution1.APMatrix, HashMatrixMixin, solution2.WritableMixin, solution2.StrValueMixin):
    pass


if __name__ == "__main__":
    a = APMatrix([[1, 2]])
    b = APMatrix([[2], [2]])
    c = APMatrix([[1, 3]])
    d = APMatrix([[2], [2]])
    assert hash(a) == hash(c)
    assert a.data != c.data
    assert b.data == d.data
    ab = a @ b
    CacheMatrixOperationsMixin.cache = {}
    cd = c @ d
    assert ab != cd
    CacheMatrixOperationsMixin.cache = {}
    # из-за кэша
    assert a @ b == c @ d
    a.write_to_file("artifacts/3.3/A.txt")
    b.write_to_file("artifacts/3.3/B.txt")
    c.write_to_file("artifacts/3.3/C.txt")
    d.write_to_file("artifacts/3.3/D.txt")
    ab.write_to_file("artifacts/3.3/AB.txt")
    cd.write_to_file("artifacts/3.3/CD.txt")
    with open("artifacts/3.3/hash.txt", "w") as f:
        f.write(f"{hash(ab)} {hash(cd)}")
