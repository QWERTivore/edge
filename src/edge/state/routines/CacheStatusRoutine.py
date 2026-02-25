from edge.core.state.Step import Step
from edge.core.state.Routine import Routine
from edge.state.commands import status_cache_mount

class CacheStatusRoutine(Routine):
  """
  Runs a single command to check the status of the cache device.
  """
  def __init__(self):
    steps = [Step(status_cache_mount.run)]

    super().__init__(steps=steps, verbose=True)