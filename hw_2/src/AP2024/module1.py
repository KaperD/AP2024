__all__ = [
    "create_latex_table",
    "create_latex_image"
]


def create_begin_table(number_of_columns):
    return f"""\\begin{{tabular}}{{ |{"|".join(["c" for _ in range(number_of_columns)])}| }}
\\hline
"""


def create_end_table():
    return r"""
\hline
\end{tabular}
"""


def create_row_separator():
    return r"""
\hline
"""


def create_row(row, number_of_columns):
    return " & ".join([str(element) for element in row] + ["" for _ in range(number_of_columns - len(row))]) + r" \\"


def create_rows(table, number_of_columns):
    return create_row_separator().join([create_row(row, number_of_columns) for row in table])


def count_columns(table):
    return max([len(row) for row in table])


def create_latex_table(table):
    return create_begin_table(count_columns(table)) + create_rows(table, count_columns(table)) + create_end_table()


def create_latex_image(path_to_image):
    return f"""
\\includegraphics[scale=1.0]{{{path_to_image}}}
"""
