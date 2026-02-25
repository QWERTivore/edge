"""
Enums used in the base class Routine that assert the actions that can be applied on chain evaluators.
"""
from enum import auto, Enum

class CommandAction(Enum):
    ABORT = auto()