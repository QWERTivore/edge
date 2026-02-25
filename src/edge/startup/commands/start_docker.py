import subprocess
from edge.core.models.ReportModels import CommandReport

def run() -> CommandReport:
  """
  Starts the Docker daemon via systemctl.
  
  Returns:
    A CommandReport with ok=True if Docker started.
    ok=False with stderr otherwise.
  """
  command = subprocess.run(
    ["systemctl", "start", "docker"],
    capture_output=True,
    text=True,
    encoding="utf-8"
  )

  report = CommandReport(
    ok = (command.returncode == 0),
    stdout = command.stdout,
    stderr = command.stderr
  )

  return report