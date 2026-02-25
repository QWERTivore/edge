import argparse

from edge.core.feedback import print_runtime_context

from edge.startup.routines.BootstrapRoutine import BootstrapRoutine
from edge.startup.routines.StartDockerRoutine import StartDockerRoutine
from edge.startup.routines.StartFrigateRoutine import StartFrigateRoutine

from edge.state.routines.CacheStatusRoutine import CacheStatusRoutine
from edge.state.routines.DockerStatusRoutine import DockerStatusRoutine
from edge.state.routines.FrigateStatusRoutine import FrigateStatusRoutine
from edge.state.routines.StorageStatusRoutine import StorageStatusRoutine

def main():
  command = argparse.ArgumentParser(
                      prog="edge",
                      description=" A control plane interface for managing \
                                   Frigate based Docker Compose deployments \
                                   on Debian systems")

  subcommand = command.add_subparsers(dest="command")

  # edge test
  subcommand.add_parser("test")

  # edge bootstrap
  subcommand.add_parser("bootstrap")

  # edge start <target>
  start = subcommand.add_parser("start")
  start_subcommand = start.add_subparsers(dest="target")
  start_subcommand.add_parser("docker")
  start_subcommand.add_parser("frigate")

  # edge status <target>
  status = subcommand.add_parser("status")
  status_subcommand = status.add_subparsers(dest="target")
  status_subcommand.add_parser("docker")
  status_subcommand.add_parser("frigate")
  status_subcommand.add_parser("cache")
  status_subcommand.add_parser("storage")

  args = command.parse_args()

  if args.command == "test":
    print("You rolled a 20 on your Strength check! Behold! All paladins stand in solemn salute as your might is recognized.")

  if args.command == "bootstrap":
    print_runtime_context(BootstrapRoutine().run())

  if args.command == "start":
    match args.target:
      case "docker":
        print_runtime_context(StartDockerRoutine().run())
      case "frigate":
        print_runtime_context(StartFrigateRoutine().run())

  if args.command == "status":
    match args.target:
      case "docker":
        print_runtime_context(DockerStatusRoutine().run())
      case "frigate":
        print_runtime_context(FrigateStatusRoutine().run())
      case "cache":
        print_runtime_context(CacheStatusRoutine().run())
      case "storage":
        print_runtime_context(StorageStatusRoutine().run())