from edge.core.state.Step import Step
from edge.core.state.Routine import Routine
from edge.state.commands import status_frigate

class FrigateStatusRoutine(Routine):
  """
  Runs a single command to check the status of the frigate container.
  """
  def __init__(self):
    steps = [Step(status_frigate.run)]

    super().__init__(steps=steps, verbose=True)