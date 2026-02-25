import unittest
from pathlib import Path
from edge.core import mutate

class TestMutateCastsStringToPath(unittest.TestCase):
  def test_mutate(self):
    self.assertEqual(mutate.filepath_as_string_to_path("some/test/path"), Path("some/test/path"))