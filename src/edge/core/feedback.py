"""
Utilities for providing feedback to users and systems.

Functions:
- running(): a print of the command that is running.
"""
from typing import Callable
from edge.core.models.RuntimeContext import RuntimeContext

def running(command: Callable):
  """
  Print a runtime message as: module_name, e.g. start_docker -> start docker
  """
  module_name = command.__module__.split(".")[-1]
  title = module_name.replace("_", " ").title()
  print(title)

def print_runtime_context(context: RuntimeContext):
  print("\n")
  for chain_id in context.reports:
    reports = context.reports[chain_id]
    print(f"{chain_id}:")

    for report in reports:
      name = report.__class__.__name__
      print(f"{name}: ok:{report.ok}, stdout:{report.stdout}, stderr:{report.stderr}\n")

  # If the routine terminated early at this chain
  if context.terminated_by is not None:
    print(f"Routine Terminated By:{context.terminated_by} @ chain_id_{context.terminated_at_chain_id}")
