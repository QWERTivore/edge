import unittest
from unittest.mock import patch
from parameterized import parameterized
from edge.startup.commands import start_docker

# Exit status codes: systemctl @ (https://www.man7.org/linux/man-pages/man1/systemctl.1.html)

class TestCommandReportOkTrueOnSystemCtlStart(unittest.TestCase):

  @patch("edge.startup.commands.start_docker.subprocess")
  def test_systemctl_start(self, mock_subprocess):
    mock_subprocess.run.return_value.returncode = 0
    mock_subprocess.run.return_value.stdout = "running_service_ok"
    mock_subprocess.run.return_value.stderr = ""
    
    report = start_docker.run()
    self.assertTrue(report.ok)
    self.assertEqual(report.stdout, "running_service_ok")
    self.assertEqual(report.stderr, "")

class TestCommandReportOkFalseOnSystemCtlStart(unittest.TestCase):
  @parameterized.expand([
    ("dead_pid_file_exists", 1, False),
    ("dead_lock_file_exist", 2, False),
    ("not_running", 3, False),
    ("status_unknown", 4, False)
  ])
  @patch("edge.startup.commands.start_docker.subprocess")
  def test_systemctl_start(self, failure_description, returncode, expected_ok, mock_subprocess):
    mock_subprocess.run.return_value.returncode = returncode
    mock_subprocess.run.return_value.stdout = ""
    mock_subprocess.run.return_value.stderr = failure_description
    
    report = start_docker.run()
    self.assertEqual(report.ok, expected_ok)
    self.assertEqual(report.stdout, "")
    self.assertEqual(report.stderr, failure_description)