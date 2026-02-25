import os
from edge.core import find
from yaml import safe_load
from edge.startup.models.StartupModels import Mount
from edge.core.models.ReportModels import MountReport

def run() -> MountReport:
  """
  Loads the storage key of the mount mapping from startup/config.startup.yml and
  checks that the path exists in the filesystem and the OS recognizes that it is mounted.

  Returns:
    A MountReport with ok=True if the filepath exists and is mounted & provides a mock stdout with report.
    ok=False with stderr otherwise.
  """
  root_dir = find.root("pyproject.toml")
  config_dir = find.from_root(root_dir, "startup.yml")
  yaml = safe_load(open(config_dir))
  mount = Mount(**yaml["mount"])

  path_exists = os.path.exists(mount.storage)
  is_mounted = os.path.ismount(mount.storage)

  report = MountReport(
    ok = path_exists & is_mounted,
    stdout = f"Path exists: {path_exists}. Path mounted: {is_mounted}" if path_exists & is_mounted else "",
    stderr = "" if path_exists & is_mounted else f"Path exists: {path_exists}. Path mounted: {is_mounted}",
    isMounted = is_mounted,
    path = mount.storage
  )

  return report