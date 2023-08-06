from typing import Callable, List

import pandas as pd

from nonion import Pipeline

from dskit.frame import FrameFunction

class ColumnFilter:
  pass

class ColumnFilter:
  def __init__(self, get: FrameFunction[List[str]] = lambda xs: xs.columns):
    self.get = get

  def __invert__(self) -> ColumnFilter:
    return invert(self)

  def __add__(self, y: ColumnFilter) -> ColumnFilter:
    return combine(self, y)

  def __call__(self, xs: pd.DataFrame) -> List[str]:
    return self.get(xs)

def invert(f: ColumnFilter) -> ColumnFilter:
  def inverse(xs: pd.DataFrame) -> List[str]:
    ys: List[str] = f(xs)
    g: FrameFunction[List[str]] = create_column_filter(lambda x: x not in ys)

    return g(xs)

  return ColumnFilter(inverse)

def combine(f: ColumnFilter, g: ColumnFilter) -> ColumnFilter:
  return ColumnFilter(lambda xs: f(xs) + g(xs))

def column(*args: str) -> ColumnFilter:
  get: FrameFunction[List[str]] = create_column_filter(lambda x: x in args)
  return ColumnFilter(get)

def create_column_filter(p: Callable[[str], bool]) -> FrameFunction[List[str]]:
  return lambda xs: Pipeline(xs.columns) % p >> list
