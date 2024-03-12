#!/usr/bin/python3
from module1 import create_latex_table


def create_begin_document():
    return r"""\documentclass{article}
\begin{document}
\begin{center}
"""


def create_end_document():
    return r"""\end{center}
\end{document}
"""


if __name__ == "__main__":
    table = [
        [1, 2, "3", "4, 5", 6.1, []],
        [],
        ["1\n2", None]
    ]
    result_document = create_begin_document() + create_latex_table(table) + \
        create_end_document()
    with open("artifacts/1-RESULT.tex", "w") as file:
        file.write(result_document)
