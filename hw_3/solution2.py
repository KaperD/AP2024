import numpy as np
import numbers
import os


class WritableMixin:
    def write_to_file(self, file) -> None:
        with open(file, "w") as f:
            f.write(str(self))


class StrValueMixin:
    def __str__(self) -> str:
        return os.linesep.join([str(value) for value in self.value])


class ReprValueMixin:
    def __repr__(self) -> str:
        return f"{type(self).__name__}({repr(self.value)})"


class Value:
    def __init__(self, value=None):
        if value is None:
            value = []
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, list):
            self._value = value
        elif isinstance(value, np.ndarray):
            self._value = value.tolist()
        else:
            raise ValueError("Value must be a list or numpy array")


class APArray(Value, np.lib.mixins.NDArrayOperatorsMixin, WritableMixin, StrValueMixin, ReprValueMixin):
    _HANDLED_TYPES = (np.ndarray, numbers.Number, list)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(
                x, self._HANDLED_TYPES + (APArray,)
            ):
                return NotImplemented

        inputs = tuple(x.value if isinstance(x, APArray) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.value if isinstance(x, APArray) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)


if __name__ == "__main__":
    np.random.seed(0)
    a = APArray(np.random.randint(0, 10, (10, 10)))
    b = APArray(np.random.randint(0, 10, (10, 10)))
    sum = a + b
    sum.write_to_file("artifacts/3.2/array+.txt")
    mul = a * b
    mul.write_to_file("artifacts/3.2/array*.txt")
    mat_mul = a @ b
    mat_mul.write_to_file("artifacts/3.2/array@.txt")
