
import ast
import sys
import typing as t

T = t.TypeVar('T')
U = t.TypeVar('U')


class maps(t.Generic[T, U]):
  """
  Map a function over a value if it is not None and return the result. Example usage:

  ```py
  value: t.Optional[int] = os.getenv('NUM_CORES') | maps(int)
  ```
  """

  def __init__(self, func: t.Callable[[T], U]) -> None:
    self._func = func

  def __ror__(self, val: t.Optional[T]) -> t.Optional[U]:
    if val is not None:
      return self._func(val)
    return None


def module(body: t.List[ast.stmt]) -> ast.Module:
  node = ast.Module(body)
  if sys.version >= '3.8':
    node.type_ignores = []  # type: ignore
  return node


def arguments(args: t.List[ast.arg]) -> ast.arguments:
  node = ast.arguments(
      args=args,
      vararg=None,
      kwonlyargs=[],
      kw_defaults=[],
      kwarg=None,
      defaults=[])
  if sys.version >= '3.8':
    node.posonlyargs = []  # type: ignore
  return node


def function_def(
  name: str,
  args: t.List[str],
  body: t.Sequence[ast.AST],
  lineno: t.Optional[int] = None,
  col_offset: t.Optional[int] = None,
) -> ast.FunctionDef:
  """
  Helper function to create a function def.
  """

  node = ast.FunctionDef(
    name=name,
    args=arguments([ast.arg(x, None) for x in args]),
    body=body,
    decorator_list=[],
    lineno=lineno,
    col_offset=col_offset)
  ast.fix_missing_locations(node)
  return node


def name_expr(
  name: str,
  ctx: ast.expr_context,
  lineno: t.Optional[int] = None,
  col_offset: t.Optional[int] = None
) -> ast.expr:
  """
  Helper function to parse a name/attribute access/indexing to an AST node.
  """

  node = t.cast(ast.Expression, ast.parse(name, mode='eval')).body
  if hasattr(node, 'ctx'):
    node.ctx = ctx  # type: ignore
  if lineno is not None:
    node.lineno = lineno
  if col_offset is not None:
    node.col_offset = col_offset
  ast.fix_missing_locations(node)
  return node


def compile_snippet(snippet: str, lineno: int, col_offset: int, mode: str = 'exec') -> t.Sequence[ast.AST]:
  """
  Compile a snippet into a Python AST.
  """

  node = ast.parse(snippet, filename='<input>', mode=mode)

  # Will be fixed later down the road with #ast.fix_missing_locations().
  for child in ast.walk(node):
    if hasattr(child, 'lineno'):
      child.lineno = lineno
      child.col_offset = col_offset

  if mode == 'exec':
    return t.cast(ast.Module, node).body

  elif mode == 'eval':
    node = t.cast(ast.Expression, ast.parse(snippet, mode='eval'))
    return [node.body]

  else:
    raise ValueError(f'bad mode: {mode!r}')
