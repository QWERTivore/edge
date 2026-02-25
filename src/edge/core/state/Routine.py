"""
The core class of the application.
"""
from copy import deepcopy
from typing import Callable
from edge.core import feedback
from edge.core.state.Step import Step
from edge.core.enums.ActionEnums import CommandAction
from edge.core.models.ReportModels import CommandReport
from edge.core.models.RuntimeContext import RuntimeContext

class Routine:
  """
  Represents Steps as command chains and makes available the CommandReport of each command module executed through a RuntimeContext.
  
  Routine is the baseclass for all routines (BootstrapRoutine etc.) in the application. 
  A Routine sequences command chain execution sequentially from a list of Steps.
  A Routine can be configured as verbose, in which case the result of a command modules excution
  will be printed to the console.
  """
  def __init__(self, steps: list[Step], verbose: bool = True):
    self.steps = steps
    self.verbose = verbose
    self.context = RuntimeContext()

  def run(self) -> RuntimeContext:
    """
    Evaluates the command chains in the list[Step] and returns a RuntimeContext
    that can be used to inspect the command module exectuion.
    """
    chain_id_index = 0

    for step in self.steps:
      # Run the first command in the chain.
      link = self._run_command(step.command)
      self.context.reports[f"chain_id_{chain_id_index}"].append(link)

      # Determine if a chain evaluator is present.
      chain_evaluator = self._find_evaluator(link, step)
      if chain_evaluator is not None:
        link = self._run_command(chain_evaluator)
        self.context.reports[f"chain_id_{chain_id_index}"].append(link)

      # Determine if an abort command action has been set.
      if self._abort(link, step):
        self.context.terminated_by = CommandAction.ABORT
        self.context.terminated_at_chain_id = chain_id_index
        return deepcopy(self.context)

      chain_id_index += 1
    
    return deepcopy(self.context)

  def _run_command(self, command: Callable) -> CommandReport:
    """
    Runs the desired command module function and outputs its status to the console if verbose was True on initilization.
    """
    if self.verbose: feedback.running(command)
    return command()

  def _find_evaluator(self, report: CommandReport, step: Step) -> Callable | None:
    """
    Evaluates the a CommandReport and a step object to identify chained commands.
    """
    # The CommandReport has an isRunning property set False and and step has a not running command.
    if hasattr(report, "isRunning") and report.isRunning is False and step.not_running_command:
      return step.not_running_command
    # The command failed and step has a not running command.
    if not report.ok and step.not_running_command:
      return step.not_running_command
    # The command failed and step has a on failure command.
    if not report.ok and step.on_failure_command:
      return step.on_failure_command

    return None

  def _abort(self, report: CommandReport, step: Step) -> bool:
    """
    Evaluates the a CommandReport and a step object to identify abort actions.
    """
    # The CommandReport has an isRunning property set False and step has an abort action.
    if hasattr(report, "isRunning") and report.isRunning is False and step.not_running_action == CommandAction.ABORT:
      return True
    # The command failed and step has an abort action.
    if not report.ok and step.on_failure_action == CommandAction.ABORT:
      return True

    return False