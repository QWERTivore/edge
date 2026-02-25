"""
Report objects communicate the feedback that a command module generates.
"""
import json
from typing import Optional
from dataclasses import asdict, dataclass

@dataclass
class CommandReport:
    """
    The base class of all reports. Represents both the real and synthetic output of a command.
    
    Synthetic output is generated in command modules when the command or module being used to perform an operation
    either A: does not use a console command (e.g. pyhton module os), B: does not output meaningful data such as a returncode, stderr or stdout.
    """
    ok: bool
    stdout: Optional[str] = None
    stderr: Optional[str] = None

    def to_json(self):
        """
        Returns the JSON representation of a command report.
        """
        return json.dumps(asdict(self))

@dataclass
class MountReport(CommandReport):
    """
    Represents a location in the file system that serves as a disc mount.
    """
    isMounted: Optional[bool] = None
    path: Optional[str] = None

@dataclass
class DockerReport(CommandReport):
    """
    Represents the output of a 'docker ps' command whose arguments assert an output format.
    
    Example:
        docker ps --filter name=frigate --format {{.Id} {{.Name}} {{.Status}}
    """
    isRunning: Optional[bool] = None
    dockerID: Optional[str] = None
    name: Optional[str] = None
    image: Optional[str] = None
    node: Optional[str] = None
    desired_state: Optional[str] = None
    current_state: Optional[str] = None
    error: Optional[str] = None
    ports: Optional[str] = None