"""
Schema objects that represent startup/config/startup.yml mappings and their keys.
"""
from typing import Optional
from dataclasses import dataclass

@dataclass
class Mount():
  """
  Represents the mount mapping keys in startup/config/startup.yml.
  """
  service: Optional[str] = None
  storage: Optional[str] = None
  cache: Optional[str] = None

@dataclass
class Configuration():
  """
  Represents the configuration mapping keys in startup/config/startup.yml.
  """
  service: Optional[str] = None
  filename: Optional[str] = None
  directory: Optional[str] = None
