import subprocess
from edge.core.models.ReportModels import CommandReport

def run() -> CommandReport:
  """
  Queries systemctl to discover if the docker service is in the running state.

  Returns:
    A CommandReport with ok=True if the Docker engine is running.
    ok=False with stderr otherwise.
  """
  command = subprocess.run(
    ["systemctl", "is-active", "docker"],
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