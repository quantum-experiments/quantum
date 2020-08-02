from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)

from quantum.evaluate import evaluate

@register_line_magic
def quantum(line):
    return evaluate(line)
