"""
Utilities for identifying the root folder of a project or directory and searching for files within it.

Functions:
- root(): Walk upward from the current modules execution directory to find a root folder.
- from_root(): Search downward from the root for a target file.
"""

from pathlib import Path

def root(filename: str) -> Path | None:
  """
  Identify the root of a project directory using a file as its anchor.
  Walk upward from this file and return the first path containing the filename.

  Args:
      filename (str): The filename used as the project's root anchor.

  Returns:
      Path: The resolved path to the file or None.
  """
  here = Path(__file__).resolve()

  for path in [here] + list(here.parents):
    target = path.joinpath(filename)
    if target.exists():
      return target
  
  return None

def from_root(root_path: Path, filename: str) -> Path | None:
  """
  Search from the root directory of a project for a file.
  
  Args:
      root_path (Path): The directory that identifies the root of the project.
      filename (str): The target file you are searching for.

  Returns:
      Path: The resolved path to the file or None.
  """
  root = root_path.parent

  for path in list(root.rglob("*")):
      if path.name == filename: 
        return path
        
  return None



