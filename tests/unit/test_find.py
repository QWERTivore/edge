import unittest
from pathlib import Path
from edge.core import find
from unittest.mock import patch
from tempfile import TemporaryDirectory

class TestFindRootReturnsTempPath(unittest.TestCase):
  def test_find_root(self):
    # Setup a temporary test directory
    with TemporaryDirectory() as temp_dir:
      path = Path(temp_dir)
      path.joinpath("a", "b", "c").mkdir(parents=True)
      path.joinpath("a", "pyproject.toml").touch()
      
      # Setup starting path for find
      with patch("edge.core.find.__file__", new = str(path.joinpath("a", "b", "c", "fake_module.py").resolve())):
        self.assertEqual(
                        find.root("pyproject.toml").resolve(), 
                        path.joinpath("a", "pyproject.toml").resolve()
                        )

class TestFindFromRootReturnsTempPath(unittest.TestCase):
  def test_find_from_root(self):
    # Setup a temporary test directory
    with TemporaryDirectory() as temp_dir:
      path = Path(temp_dir)
      path.joinpath("a", "b", "c").mkdir(parents=True)
      path.joinpath("a", "pyproject.toml").touch()
      path.joinpath("a", "b", "c", "startup.yml").touch()

      # Setup starting path for find
      with patch("edge.core.find.__file__", new = str(path.joinpath("a", "b", "c", "fake_module.py").resolve())):
        self.assertEqual(
                        find.from_root(find.root("pyproject.toml"), "startup.yml").resolve(), 
                        path.joinpath("a", "b", "c", "startup.yml").resolve()
                        )