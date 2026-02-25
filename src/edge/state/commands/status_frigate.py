import re, subprocess
from edge.core.models.ReportModels import DockerReport

def run() -> DockerReport:
  """
  Queries the Docker engine to discover if the frigate container is in the running state.

  Returns:
    A DockerReport with ok=True if the command completed successfully and isRunning=True if the Docker cli output indicated
    any variation of the word 'running' in its .DesiredState argument to --format.
    ok=False with stderr otherwise.
  """
  command = subprocess.run(
    ["docker", "ps", "--filter", "name=frigate", "--format", "{{.ID}} {{.Names}} {{.Status}}"],
    capture_output=True,
    text=True,
    encoding="utf-8"
  )

  # Default values
  container_id = container_name = container_state = container_error = is_running = None

  # Join dockers output with a list of keys
  if command.stdout != "": 
    output = command.stdout.strip().split(maxsplit=2) # strip() no newline or extra spaces, split() at most three parts.
    keys = ["id", "name", "status"]
    data = dict(zip(keys, output))

    container_id = data.get("id")
    container_name = data.get("name")
    container_state = data.get("status")
    is_running = bool(re.search(pattern=r"up", string=container_state, flags=re.IGNORECASE))

  report = DockerReport(
    ok = (command.returncode == 0),
    stdout = command.stdout,
    stderr = command.stderr,
    isRunning = is_running,
    dockerID = container_id,
    name = container_name,
    desired_state = container_state
  )

  return report