from edge.core.state.Step import Step
from edge.core.state.Routine import Routine
from edge.core.enums.ActionEnums import CommandAction
from edge.startup.commands import start_docker, start_frigate
from edge.state.commands import status_storage_mount, status_cache_mount, status_docker, status_frigate

class BootstrapRoutine(Routine):
  """
  Checks disc mounts and docker's status before starting frigate.
  """
  def __init__(self):
    steps = [
          Step(status_storage_mount.run).on_failure_do(CommandAction.ABORT),
          Step(status_cache_mount.run).on_failure_do(CommandAction.ABORT),
          Step(status_docker.run).not_running_do(start_docker.run).on_failure_do(CommandAction.ABORT),
          Step(start_frigate.run).on_failure_do(CommandAction.ABORT),
          Step(status_frigate.run)]

    super().__init__(steps=steps, verbose=True)