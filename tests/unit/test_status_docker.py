import unittest
from unittest.mock import patch
from parameterized import parameterized
from edge.state.commands import status_docker

class TestCommandReportOkTrueOnSystemCtlIsActive(unittest.TestCase):
  @patch("edge.state.commands.status_docker.subprocess")
  def test_status_docker(self, mock_subprocess):
    mock_subprocess.run.return_value.returncode = 0
    mock_subprocess.run.return_value.stdout = "some_status_ok"
    mock_subprocess.run.return_value.stderr = ""

    report = status_docker.run()
    self.assertTrue(report.ok)
    self.assertEqual(report.stdout, "some_status_ok")
    self.assertEqual(report.stderr, "")

class TestCommandReportOkFalseOnSystemCtlIsActive(unittest.TestCase):
  @parameterized.expand([
    ("dead_pid_file_exists", 1, False),
    ("dead_lock_file_exist", 2, False),
    ("not_running", 3, False),
    ("status_unknown", 4, False)
  ])
  @patch("edge.state.commands.status_docker.subprocess")
  def test_status_docker(self, failure_description, returncode, expected_ok, mock_subprocess):
    mock_subprocess.run.return_value.returncode = returncode
    mock_subprocess.run.return_value.stdout = ""
    mock_subprocess.run.return_value.stderr = failure_description

    report = status_docker.run()
    self.assertEqual(report.ok, expected_ok)
    self.assertEqual(report.stdout, "")
    self.assertEqual(report.stderr, failure_description)