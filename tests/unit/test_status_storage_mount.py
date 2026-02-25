import unittest
from pathlib import Path
from unittest.mock import patch
from tempfile import TemporaryDirectory
from edge.state.commands import status_storage_mount

class TestStorageOsPathExistsTrueAndIsMountTrue(unittest.TestCase):
  @patch("edge.state.commands.status_storage_mount.os.path.exists")
  @patch("edge.state.commands.status_storage_mount.os.path.ismount")
  def test_status_storage_mount(self, mock_ismount, mock_exists):
    # Setup a temporary test directory
    with TemporaryDirectory() as temp_dir:
      path = Path(temp_dir)
      path.joinpath("a", "b", "c").mkdir(parents=True)
      path.joinpath("a", "pyproject.toml").touch()
      
      # Create a test version of a startup.yml file
      path.joinpath("a", "b", "startup.yml").touch()
      path.joinpath("a", "b", "startup.yml").write_text("mount:\n  storage: /mnt/fake-mount\n")

      # Setup starting path for find
      with patch("edge.core.find.__file__", new = str(path.joinpath("a", "b", "c", "fake_module.py").resolve())):
        mock_exists.return_value = True
        mock_ismount.return_value = True
        
        report = status_storage_mount.run()
        self.assertTrue(report.ok)
        self.assertEqual(report.stdout, "Path exists: True. Path mounted: True")
        self.assertEqual(report.stderr, "")
        self.assertTrue(report.isMounted)
        self.assertEqual(report.path, "/mnt/fake-mount")

class TestStorageOsPathExistsTrueAndIsMountFalse(unittest.TestCase):
  @patch("edge.state.commands.status_storage_mount.os.path.exists")
  @patch("edge.state.commands.status_storage_mount.os.path.ismount")
  def test_status_storage_mount(self, mock_ismount, mock_exists):
    # Setup a temporary test directory
    with TemporaryDirectory() as temp_dir:
      path = Path(temp_dir)
      path.joinpath("a", "b", "c").mkdir(parents=True)
      path.joinpath("a", "pyproject.toml").touch()
      
      # Create a test version of a startup.yml file
      path.joinpath("a", "b", "startup.yml").touch()
      path.joinpath("a", "b", "startup.yml").write_text("mount:\n  storage: /mnt/fake-mount\n")

      # Setup starting path for find
      with patch("edge.core.find.__file__", new = str(path.joinpath("a", "b", "c", "fake_module.py").resolve())):
        mock_exists.return_value = True
        mock_ismount.return_value = False

        report = status_storage_mount.run()
        self.assertFalse(report.ok)
        self.assertEqual(report.stdout, "")
        self.assertEqual(report.stderr, "Path exists: True. Path mounted: False")
        self.assertFalse(report.isMounted)
        self.assertEqual(report.path, "/mnt/fake-mount")