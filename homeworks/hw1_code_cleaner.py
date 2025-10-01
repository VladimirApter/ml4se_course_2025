"""
Модель: ChatGPT 5 Instant
Промпт:
У меня есть исходный код программы на python. Нужно подготовить его для анализа, а конкретно:
1. Убрать все комментарии
2. Заменить табуляцию на пробелы, а лишние пробелы убрать
3. Имена переменных, функций и классов заменить на такие: "name_i", где i - порядковый номер переменной, функции или класса.

Для примера рассмотри такой код в виде строки:
"import math  # comment\n\nmy_variable = 10\ndef my_function(x):\n\treturn my_variable + x\n\nclass MyClass:\n    pass\n"

После обработки он должен выглядеть так:
"import math\nname_1 = 10\n\ndef name_2(name_3):\n    return name_1 + name_3\n\nclass name_4:\n    pass\n"

Напиши программу на python, которая будет подобным образом обрабатывать строковое представление кода.
"""

import ast
from typing import Dict


class Renamer(ast.NodeTransformer):
    def __init__(self) -> None:
        self.mapping: Dict[str, str] = {}
        self.counter = 0
        super().__init__()

    def _bind(self, original: str) -> str:
        if original not in self.mapping:
            self.counter += 1
            self.mapping[original] = f"name_{self.counter}"
        return self.mapping[original]

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        node.name = self._bind(node.name)
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.AST:
        node.name = self._bind(node.name)
        self.generic_visit(node)
        return node

    def visit_Name(self, node: ast.Name) -> ast.AST:
        node.id = self._bind(node.id)
        return node

    def visit_arg(self, node: ast.arg) -> ast.AST:
        node.arg = self._bind(node.arg)
        return node


def process_code(code_str: str) -> str:
    tree = ast.parse(code_str)
    tree = Renamer().visit(tree)
    ast.fix_missing_locations(tree)
    return ast.unparse(tree)


if __name__ == "__main__":
    src = (
        "import math  # comment\n\nmy_variable = 10\ndef my_function(x):\n\treturn my_variable + x\n\nclass MyClass:\n    pass\n"
    )
    print(process_code(src))
