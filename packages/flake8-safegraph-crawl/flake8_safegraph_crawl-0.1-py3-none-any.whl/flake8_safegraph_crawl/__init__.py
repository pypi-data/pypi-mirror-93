import ast
import sys
from typing import Any, Generator, List, Tuple, Type


if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata


class Visitor(ast.NodeVisitor):
    def __init__(self):
        self.problems: List[Tuple[int, int]] = []

    def visit_Import(self, node: ast.Import) -> None:
        if any(alias.name == "requests" for alias in node.names):
            self.problems.append((node.lineno, node.col_offset))
        self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)
        for line, col in visitor.problems:
            yield (
                line,
                col,
                "SG100 imports 'requests' module. Please use 'sgrequests' instead",
                type(self),
            )
