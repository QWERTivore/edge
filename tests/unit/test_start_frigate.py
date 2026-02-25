import unittest
from unittest.mock import patch
from edge.startup.commands import start_frigate

class TestCommandReportOkTrueOnDockerComposeUp(unittest.TestCase):
  @patch("edge.startup.commands.start_frigate.subprocess")
  def test_docker_up(self, mock_subprocess):
    mock_subprocess.run.return_value.returncode = 0
    mock_subprocess.run.return_value.stdout = "frigate running..."
    mock_subprocess.run.return_value.stderr = ""

    report = start_frigate.run()
    self.assertTrue(report.ok)
    self.assertEqual(report.stdout, "frigate running...")
    self.assertEqual(report.stderr, "")

class TestCommandReportOkFalseOnDockerComposeUp(unittest.TestCase):
  @patch("edge.startup.commands.start_frigate.subprocess")
  def test_docker_up(self, mock_subprocess):
    mock_subprocess.run.return_value.returncode = 1
    mock_subprocess.run.return_value.stdout = ""
    mock_subprocess.run.return_value.stderr = "mock_error"

    report = start_frigate.run()
    self.assertFalse(report.ok)
    self.assertEqual(report.stdout, "")
    self.assertEqual(report.stderr, "mock_error")