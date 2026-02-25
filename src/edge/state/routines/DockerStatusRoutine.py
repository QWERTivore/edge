from edge.core.state.Step import Step
from edge.core.state.Routine import Routine
from edge.state.commands import status_docker

class DockerStatusRoutine(Routine):
  """
  Runs a single command to check the status of docker.
  """
  def __init__(self):
    steps = [Step(status_docker.run)]

    super().__init__(steps=steps, verbose=True)