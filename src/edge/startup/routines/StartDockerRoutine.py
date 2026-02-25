from edge.core.state.Step import Step
from edge.core.state.Routine import Routine
from edge.startup.commands import start_docker

class StartDockerRoutine(Routine):
  """
  Runs a single command to start docker.
  """
  def __init__(self):
    steps = [Step(start_docker.run)]

    super().__init__(steps=steps, verbose=True)