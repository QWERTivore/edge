"""
Step describes a sequence of command module/s execution. 
"""
from typing import Callable
from edge.core.enums.ActionEnums import CommandAction

class Step:
  """
  Represents a command chain.

  A command chain describes a sequence of command module/s to execute.
  A command chain can have a chain evaluator. A chain evaluator is a declarative
  action expression that triggers some behavior.

  Chain evaluators (not_running_do, on_failure_do) can only be called once per Step.
  Attempting to set the same evaluator twice raises a ValueError.

  Note: 
    You may invoke a single command module without chain evaluators.

  Usage:
    Step(command_module.run)
    Step(command_module.run).not_running_do(command_module.run | CommandAction).on_failure_do(command_module.run | CommandAction)
  """
  def __init__(self, command: Callable):
    self.command = command
    self.not_running_command = None
    self.not_running_action = None
    self.on_failure_command = None
    self.on_failure_action = None

  def not_running_do(self, handler: Callable | CommandAction):
    """
    A chain evaluator that asserts the mechanism to apply when a command modules Report
    indicates that a process is not in the running state.
    """
    if self.not_running_command is not None or self.not_running_action is not None:
        raise ValueError("not_running_do already set")

    if callable(handler):
      self.not_running_command = handler
    if isinstance(handler, CommandAction):
      self.not_running_action = handler
    return self

  def on_failure_do(self, handler: Callable | CommandAction):
    """
    A chain evaluator that asserts the mechanism to apply when a command modules Report
    indicates that a process has failed to execute.
    """
    if self.on_failure_command is not None or self.on_failure_action is not None:
        raise ValueError("on_failure_do already set")
    
    if callable(handler):
        self.on_failure_command = handler
    if isinstance(handler, CommandAction):
        self.on_failure_action = handler
    return self