from edge.core.state.Step import Step
from edge.core.state.Routine import Routine
from edge.startup.commands import start_frigate

class StartFrigateRoutine(Routine):
  """
  Runs a single command to start frigate.
  """
  def __init__(self):
    steps = [Step(start_frigate.run)]

    super().__init__(steps=steps, verbose=True)