import unittest
from unittest.mock import patch
from edge.state.commands import status_frigate

class TestDockerReportCompleteAndOKTrueOnDockerServicePs(unittest.TestCase):
  @patch("edge.state.commands.status_frigate.subprocess")
  def test_status_frigate(self, mock_subprocess):
    mock_subprocess.run.return_value.stdout = "fake_id fake_service_name fake up 30s"
    mock_subprocess.run.return_value.returncode = 0
    mock_subprocess.run.return_value.stderr = ""

    report = status_frigate.run()
    self.assertTrue(report.ok)
    self.assertTrue(report.stdout, "fake_id fake_service_name fake up 30s")
    self.assertEqual(report.stderr, "")
    self.assertTrue(report.isRunning)
    self.assertEqual(report.dockerID, "fake_id")
    self.assertEqual(report.name, "fake_service_name")
    self.assertEqual(report.desired_state, "fake up 30s")