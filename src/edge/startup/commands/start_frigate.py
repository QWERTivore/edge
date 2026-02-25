import subprocess
from edge.core import find
from yaml import safe_load
from edge.core import mutate
from edge.core.models.ReportModels import CommandReport
from edge.startup.models.StartupModels import Configuration

def run() -> CommandReport:
  """
  Starts the Docker frigate container specified in the docker-compose.yml file.
  
  Returns:
    A CommandReport with ok=True if the Docker container started.
    ok=False with stderr otherwise.
  """
  # Load the fields from the startup configuration file
  root_dir = find.root("pyproject.toml")
  config_dir = find.from_root(root_dir, "startup.yml")
  yaml = safe_load(open(config_dir))
  yaml_field = Configuration(**yaml["configuration"])

  docker_compose_file = find.from_root(mutate.filepath_as_string_to_path(yaml_field.directory), yaml_field.filename)

  command = subprocess.run(
    ["docker", "compose", "-f", docker_compose_file, "up", "-d", yaml_field.service],
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
