# Edge “IS”

Edge is a highly configurable, easily extensible, fork-freindly, declarative command-line control plane for managing Frigate‑based Docker Compose deployments on Debian systems. Its automation capabilities come from four core building blocks: routines, steps, command chains, and chain evaluators.

- **Routine**: Sequences command chain execution from a list of Steps. When verbose mode is enabled, each command module’s output is printed to the console.

- **Step**: Represents a single command chain.

- **Command Chain**: Describes one or more command modules or actions to execute.
  A command chain may include a chain evaluator, which is a declarative action expression that triggers additional behavior.

---

# Edge “IS NOT”

- a GUI
- a full OS deployment utility
- a dependency or version-control utility
- a full orchestration system like Kubernetes

---

# Edge “ENABLES”

Edge is not just a CLI for Frigate — it is a flexible, composable execution engine. Because every command module returns a typed CommandReport and routines store them in a RuntimeContext, you can:

- Build daemons or automation layers that monitor system state and react dynamically.
- Extend Edge to new domains (containers, storage systems, microservices) without changing the core engine.
- Chain commands for reliable, self-healing workflows.
- Inspect execution programmatically, making it ideal for obeservability, logging, or custom notifications.

Edge provides a foundation for autonomous, type-aware orchestration, not just a wrapper around commands. The CLI is convenient, but the real power comes from what you build on top of it.

---

# Getting Started

Before using Edge, you’ll need to install the software listed in the [Dependencies](#dependencies) section.  
It is especially important that your Frigate installation and Docker Compose layout follow the standard Frigate directory convention:

```
frigate/
├── docker-compose.yml
└── config/
    └── config.yml
```

A complete guide to the recommended Frigate structure can be found here: https://docs.frigate.video/frigate/installation/

Once your Frigate deployment is configured and working, clone this repository:

```bash
git clone https://github.com/QWERTivore/edge.git
cd /your_path/edge # Change path to the root of the project.
```

## Configure the Startup File

To configure the target Docker Compose filepaths and disk‑mount locations that Edge validates during the BootstrapRoutine and various status checks (`edge status cache`, `edge start frigate`, etc.), locate and modify the `startup.yml` file:

```
edge/
└── startup/
    └── config/
        └── startup.yml
```

If you are **not using external mounts** (e.g. a NAS for video storage or a USB device for Frigate’s cache), you can ignore the mount‑related fields. However, it is **critical** that the mapping keys and their nested values in this file match your actual Frigate and Docker Compose configuration. Incorrect paths or filenames will cause routines to fail or behave unpredictably.

If you are running Frigate entirely on local storage and want to customize how routines behave, refer to the section [Customizing the App](#customizing-the-app).

---

## Configure Edge

```bash
cp /your_path/pyprojects.toml /your_path/src/edge # Copy pyproject.toml into the package so Poetry includes it in the wheel; Poetry only packages files inside src/edge/.
poetry build # Build the wheel.
pipx install dist/the_name_of_the_wheel.whl # Install the wheel into a pipx virtual environment.
pipx list # Show where pipx installed the venv.
sudo ln -s /your_path/pipx_list_location /usr/local/bin/edge # Symlink the pipx-installed executable into /usr/local/bin; so root and systemd can find it.
edge test # Test that the CLI is globally accessible.
```

# Using Edge

All command modules in Edge run through a subclass of a **Routine**. When you execute a command, Edge follows a consistent pattern:

```bash
edge <command> <target>
<command module name> # If in verbose mode (configured in the class).

<RoutineClass>: ok:<returncode>, stdout:<stdout>, stderr:<stderr>
Terminated By: <CommandAction.Abort> @ Chain ID: <ID> # If a chain evaluator triggers an action.

```

## Supported Commands:

- `edge test`
  - A simple console print. Used to validate that edge can be called at the OS level.

- `edge bootstrap`
  - Validate system configuration and bring up the entire Frigate stack.

- `edge start docker`
  - Use systemctl to start the docker service.

- `edge start frigate`
  - Uses Docker Compose to start the frigate container specified in the docker-compose.yml file.

- `edge status docker`
  - Query systemctl for dockers status.

- `edge status frigate`
  - Return a formatted docker ps output showing the status of the Frigate container.

- `edge status cache`
  - Check that the cache mount is both present and mounted

- `edge status storage`
  - Check that the storage mount is both present and mounted

---

# Customizing the App

Edge attempts to provide a unified command‑line control plane interface that simplifies Docker container management. It is most similar to declarative command‑line orchestration APIs, but its domain is intentionally thin, giving it explicit architecture, clean boundaries, and no hidden state. This is also why Edge is so fork‑friendly: if you want to adapt Edge to a different problem domain, its strict separation of concerns makes that trivial.

## Edge Problem Domains Overview:

<details>
<summary>Domain Diagram</summary>

```
                     ┌────────────────────────────┐
                     │            Edge            │
                     │ Declarative Control Plane  │
                     └──────────────┬─────────────┘
                                    │
                                    ▼
         ┌─────────────────────────────────────────────────────┐
         │                    Problem Domains                  │
         ├──────────────────────────┬──────────────────────────┤
         │   Storage Domain         │   Container Domain       │
         │   (NAS, USB mounts)      │   (Docker Compose stack: │
         │                          │    Frigate, InfluxDB,    │
         │                          │    Grafana, etc.)        │
         └──────────────────────────┴──────────────────────────┘
                                    │
                                    ▼
                     ┌────────────────────────────┐
                     │   Host System Domain       │
                     │   Debian 13 on HP t630     │
                     └────────────────────────────┘

```

</details>

## System Design Diagrams

<details>
<summary>Application File Structure</summary>

```
src/
└──edge/
   ├── __main__.py                          # Entrypoint (calls cli's main()).
   ├── cli.py                               # CLI: argparse command definitions.
   ├── core/
   │   ├── feedback.py                      # Console output utilities.
   │   ├── find.py                          # File and path discovery utilities.
   │   ├── mutate.py                        # Data transformation utilities.
   │   ├── enums/
   │   │   └── ActionEnums.py               # Command chain actions (ABORT, etc.).
   │   ├── models/
   │   │   ├── ReportModels.py              # Command output schemas (CommandReport, MountReport, DockerReport).
   │   │   └── RuntimeContext.py            # Reports and termination state.
   │   └── state/
   │       ├── Routine.py                   # The core of the application. Base class: command chain executor.
   │       └── Step.py                      # Declarative command chain definition.
   ├── startup/
   │   ├── commands/
   │   │   ├── start_docker.py              # systemctl start docker.
   │   │   └── start_frigate.py             # docker compose up frigate.
   │   ├── config/
   │   │   └── startup.yml                  # Mount paths and Docker Compose configuration.
   │   ├── models/
   │   │   └── StartupModels.py             # YAML schema models (Mount, Configuration).
   │   └── routines/
   │       ├── BootstrapRoutine.py          # Full Frigate startup sequence.
   │       ├── StartDockerRoutine.py        # Docker-only startup.
   │       └── StartFrigateRoutine.py       # Frigate-only startup.
   └── state/
       ├── commands/
       │   ├── status_cache_mount.py        # Validates cache mounts.
       │   ├── status_docker.py             # Query Docker daemon state.
       │   ├── status_frigate.py            # Query Frigate container state.
       │   └── status_storage_mount.py      # Validates storage mounts.
       └── routines/
           ├── CacheStatusRoutine.py        # Cache mount status check.
           ├── DockerStatusRoutine.py       # Docker daemon status check.
           ├── FrigateStatusRoutine.py      # Frigate container status check.
           └── StorageStatusRoutine.py      # Storage mount status.
```

</details>

<details>
<summary>Unit Test File Structure</summary>

```
tests/
└── unit/
    ├── test_find.py                         # Validates file and path resolution from a project root.
    ├── test_mutate.py                       # Validates string-to-path and data transformation utilities.
    ├── test_routine.py                      # Validates the command chain executor against all state transitions.
    ├── test_start_docker.py                 # Mocks systemctl to validate Docker start command output.
    ├── test_start_frigate.py                # Mocks docker compose to validate Frigate start command output.
    ├── test_status_cache_mount.py           # Mocks os.path to validate cache mount status reporting.
    ├── test_status_docker.py                # Mocks systemctl to validate Docker daemon status reporting.
    ├── test_status_frigate.py               # Mocks docker CLI to validate Frigate container status reporting.
    └── test_status_storage_mount.py         # Mocks os.path to validate storage mount status reporting.
```

</details>

## Extending the System

A **command module** is the atomic unit of the application. It is a Python function (typically defined in a module such as `startup/commands/start_docker.py`) that performs a single operation and returns a **ReportModel**.

A **ReportModel** is a command schema. All ReportModels inherit from **CommandReport**. A CommandReport and any subclass of, represents both the real and synthetic output of a command. Synthetic output is generated in command modules when the imported module being used to perform an operation either A: does not use a console command (e.g. Python module: os), B: does not output meaningful data such as a returncode, stderr or stdout. ReportModels are stored in a **RuntimeContext**. A RuntimeContext stores the ReportModels returned from each command in a **Routine**.

A **Routine** is a sequence of **Step** objects. It executes each step in order, collects their CommandReports into a RuntimeContext, and exposes the results to the CLI layer. All routines (e.g., BootstrapRoutine) inherit from the Routine base class.

A **Step** defines a command chain — a sequence of one or more command modules or actions to execute. A command chain describes a sequence of command module/s to execute. A command chain can have a chain evaluator. A chain evaluator is a declarative action expression that triggers some behavior. Chain evaluators (`not_running_do, on_failure_do`) can only be applied once per Step. Attempting to set the same evaluator twice raises a ValueError.

To create a Routine, subclass it and initilize it with a list of Steps. At most, a Step requires a command. Chain evaluators can be linked to the command to drive behavior. Routine evaluates each command chain and appends to the dictionary of a runtime context each command chain as: `{key:chain_id_n, value:list[CommandReports]}`.

```python
class BootstrapRoutine(Routine):
  """
  Checks disc mounts and docker's status before starting frigate.
  """
  def __init__(self):
    steps = [
          Step(status_storage_mount.run).on_failure_do(CommandAction.ABORT),
          Step(status_cache_mount.run).on_failure_do(CommandAction.ABORT),
          Step(status_docker.run).not_running_do(start_docker.run).on_failure_do(CommandAction.ABORT),
          Step(start_frigate.run).on_failure_do(CommandAction.ABORT),
          Step(status_frigate.run)]

    super().__init__(steps=steps, verbose=True)
```

Routines are executed in `src/edge/cli.py`. The cli uses argparse.ArgumentParser to structure the inputs to edge. The cli defines three argument layers: `edge, command, and target`. These parsers wrap Routines with the feedback function `print_runtime_context` to console out the results of a Routine.

```python
if args.command == "start":
    match args.target:
      case "docker":
        print_runtime_context(StartDockerRoutine().run())
      case "frigate":
        print_runtime_context(StartFrigateRoutine().run())
```

The folder structure of Edge is designed to communicate problem domains. It is self‑documenting and self‑contained. If your problem domain does not fit the existing folder names, create a new top‑level domain folder and add subfolders for the commands, routines, models, and configuration that domain requires. Commands represent the atomic operations a routine can orchestrate. In most cases, the **core** package provides everything you need to implement a new domain cleanly.

---

# Dependencies

- Debian **13.3.x**
- Python **3.14**
- Poetry **2.3.x**
- pipx **1.7.x**
- Frigate **0.16.x**

---

# Notes

Edge was created to solve a real pain point I had when managing my Frigate deployment on a thin client (HP t630) running Debian and serving as both my NVR and telemetry service. It also ended up adding value to my portfolio by demonstrating my skills in Python and infrastructure tooling development. While I do not plan to actively maintain this project, I may occasionally update it.

I encourage forking and extending. Edge is small enough not to get lost in, and its clear boundaries make it worth investing time into. If you decide to enhance the project because you like what you see, feel free to open an issue — we can coordinate your feature integration into the project.
