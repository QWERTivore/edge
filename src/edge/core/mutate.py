"""
Utilities for mutating object types.

Functions:
- filepath_as_string_to_path(): Convert a filepath to a path object.
"""

from pathlib import Path

def filepath_as_string_to_path(filepath: str) -> Path:
  """
  Mutate a string that represents a filepath to a Path object.
  """
  mutate = Path(filepath)
  return mutate