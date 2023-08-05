
"""
Transpiles a Kahmi DSL AST into a pure Python AST.
"""

import ast as pyast
import builtins
import typing as t
from dataclasses import dataclass

from . import ast, parser, util
from .macros import MacroPlugin

@dataclass
class Transpiler:

  lookup_func_name: str = '__lookup__'
  context_var_name: str = 'self'

  def transfer_loc(self, loc: ast.Location, node: pyast.AST) -> None:
    node.lineno = loc.lineno
    node.col_offset = loc.colno
    pyast.fix_missing_locations(node)

  def transpile_module(self, module: ast.Module) -> pyast.Module:
    nodes: t.List[pyast.stmt] = list(self.transpile_nodes(module.body))
    pyast_module = util.module(nodes)
    pyast.fix_missing_locations(pyast_module)
    return pyast_module

  def transpile_nodes(self, nodes: t.Iterable[ast.Node]) -> t.Iterator[pyast.stmt]:
    for node in nodes:
      if isinstance(node, ast.Let):
        yield from self.transpile_let(node)
      elif isinstance(node, ast.Call):
        yield from self.transpile_call(node)
      elif isinstance(node, ast.Assign):
        yield from self.transpile_assign(node)
      else:
        raise RuntimeError(f'encountered unexpected node: {node!r}')

  def transpile_call(self, node: ast.Call) -> t.Iterator[pyast.stmt]:
    if node.body:
      func_name = '__configure_' + node.target.name.replace('.', '_')
      body = list(self.transpile_nodes(node.body))
      yield util.function_def(
        func_name, [self.context_var_name], body,
        lineno=node.loc.lineno, col_offset=node.loc.colno)

    yield from [x.fdef for x in node.lambdas]

    target = self.transpile_target(None, node.target, pyast.Load())

    # Generate a call expression for the selected method.
    if node.args is not None:
      target = pyast.Call(
        # TODO(NiklasRosenstein): We need to decide whether to prefix it with self() or not.
        func=target,
        args=node.args,
        keywords=[],
        lineno=node.loc.lineno,
        col_offset=node.loc.colno)

    if node.body:
      value_name = func_name + '_' + self.context_var_name + '_target'
      yield pyast.Assign(targets=[util.name_expr(value_name, pyast.Store())], value=target)

      # If the value appears to be a context manager, enter it's context before executing
      # the body of the call.
      yield from t.cast(t.List[pyast.stmt], util.compile_snippet(
        f'if hasattr({value_name}, "configure"):\n'
        f'  {value_name}.configure({func_name})\n'
        f'else:\n'
        f'  {value_name}({func_name})\n',
        lineno=node.loc.lineno,
        col_offset=node.loc.colno))

    else:
      yield pyast.Expr(target)

  def transpile_assign(self, node: ast.Assign) -> t.Iterator[pyast.stmt]:
    target = self.transpile_target(self.context_var_name, node.target, pyast.Store())
    yield from [x.fdef for x in node.value.lambdas]
    yield pyast.Assign(targets=[target], value=node.value.expr.body)

  def transpile_let(self, node: ast.Let) -> t.Iterator[pyast.stmt]:
    target = self.transpile_target(None, node.target, pyast.Store())
    yield from [x.fdef for x in node.value.lambdas]
    yield pyast.Assign(targets=[target], value=node.value.expr.body)

  def transpile_target(self,
    prefix: t.Optional[str],
    node: ast.Target,
    ctx: pyast.expr_context
  ) -> pyast.expr:
    """
    Converts an #ast.Target node into an expression that identifies the target with the specified
    context (load/store/del).
    """

    name = node.name
    if prefix is not None:
      name = prefix + '.' + name

    if isinstance(ctx, pyast.Store) or prefix:
      return util.name_expr(name, ctx)

    parts = name.split('.')
    code = f'{self.lookup_func_name}({parts[0]!r}, locals(), {self.context_var_name})'
    if len(parts) > 1:
      code += '.' + '.'.join(parts[1:])
    return util.name_expr(code, ctx, lineno=node.loc.lineno, col_offset=node.loc.colno)

  def transpile_expr(self, node: ast.Expr) -> t.Tuple[t.List[pyast.FunctionDef], pyast.expr]:
    return [x.fdef for x in node.lambdas], node.expr.body


def _lookup(name: str, *scopes: t.Any) -> None:
  objs = []
  for scope in scopes:
    if isinstance(scope, dict):
      if name in scope:
        return scope[name]
    else:
      try:
        return getattr(scope, name)
      except AttributeError:
        pass
      objs.append(scope)
  try:
    return getattr(builtins, name)
  except AttributeError:
    pass

  msg = f'lookup for {name!r} failed, checked locals and:'
  for obj in objs:
    msg += f'\n  - {type(obj).__name__!r}'
  msg += '\n  - builtins'
  raise NameError(msg)


def run_file(
  context: t.Any,
  globals: t.Dict[str, t.Any],
  filename: str,
  fp: t.Optional[t.TextIO] = None,
  macros: t.Optional[t.Dict[str, MacroPlugin]] = None,
) -> None:

  globals['__lookup__'] = _lookup
  globals['self'] = context

  module = compile_file(filename, fp, macros)
  code = compile(module, filename=filename, mode='exec')
  exec(code, globals)


def compile_file(
  filename: str,
  fp: t.Optional[t.TextIO] = None,
  macros: t.Optional[t.Dict[str, MacroPlugin]] = None,
) -> pyast.Module:

  if fp is None:
    with open(filename, 'r') as fp:
      return compile_file(filename, fp, macros)

  module = parser.Parser(fp.read(), filename, macros).parse()
  return Transpiler().transpile_module(module)


__all__ = ['Transpiler', 'run_file', 'compile_file']
