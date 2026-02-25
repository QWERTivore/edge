from edge.core.state.Step import Step
from edge.core.state.Routine import Routine
from edge.state.commands import status_storage_mount

class StorageStatusRoutine(Routine):
  """
  Runs a single command to check the status of the storage device.
  """
  def __init__(self):
    steps = [Step(status_storage_mount.run)]

    super().__init__(steps=steps, verbose=True)