import ast

class FlattenNestedOps(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.new_assignments = []

    def _get_new_var(self):
        var_name = f"v{self.counter}"
        self.counter += 1
        return ast.Name(id=var_name, ctx=ast.Store())

    def _flatten_node(self, node):
        if isinstance(node, (ast.UnaryOp, ast.BinOp, ast.Call)):
            new_var = self._get_new_var()
            self.new_assignments.append(ast.Assign(targets=[new_var], value=node))
            return ast.Name(id=new_var.id, ctx=ast.Load())
        return node

    def visit_FunctionDef(self, node):
        # Cброс счетчика и назначение нового для каждой функции
        self.counter = 0
        self.new_assignments = []

        self.generic_visit(node)

        # Добавление новых назначений в начало тела функции
        node.body = self.new_assignments + node.body

        return node

    def visit_Return(self, node):
        if isinstance(node.value, (ast.Tuple, ast.List)):
            # Обработка возвратов кортежа или списка
            node.value.elts = [self._flatten_node(elt) for elt in node.value.elts]
        else:
            node.value = self._flatten_node(node.value)
        return node

    def visit_Assign(self, node):
        node.value = self._flatten_node(node.value)
        return node

    def visit_Call(self, node):
        node.args = [self._flatten_node(arg) for arg in node.args]
        return node

# Пример использования
source_code = """
def foo(a, b, c, d):
    return baz(-a, c**(a - b) + d, k=A + 123)

def bar(x):
    a = x * 2 + sin(x)
    b = a
    return a, b, x + 1
"""

tree = ast.parse(source_code)
transformer = FlattenNestedOps()
new_tree = transformer.visit(tree)
ast.fix_missing_locations(new_tree)

# Преобразование измененного AST обратно в исходный код
import astor
transformed_code = astor.to_source(new_tree)
print(transformed_code)
