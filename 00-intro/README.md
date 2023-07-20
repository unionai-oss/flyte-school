# Flyte Module 0: A Practical Introduction to Machine Learning Orchestration

This module provides a hands-on introduction to Flyte, an open source machine
learning and data processing orchestration platform. We'll cover the basics of
Flyte and how to use it locally for iterative development.

### Learning Objectives

- 🧱 Understand how tasks, workflows, and launchplans can be used to manage the
  flow of data and models through a sequence of computations.
- 💻 Learn how to spin up a local Flyte cluster on their own workstation and run
  workflows on it for local debugging.
- 🔄 Programmatically run tasks and workflows through the CLI or in a Python
  runtime to quickly iterate on your code.

## Outline

| 🔤 Introduction to Flyte | [45 minutes] |
| --- | --- |
| **Environment Setup** | Setting up your virtual development environment |
| **Flyte Basics** | Tasks, Workflows, and Launch Plans: the building blocks of Flyte |
| **`pyflyte run`** | Run tasks and workflows locally or on a Flyte cluster  |
| **Flyte Console** | A tour of the Flyte console to view workflow progress and status  |
| **`FlyteRemote`** | Programmatically run tasks and workflows  |
| **Scheduling Launch Plans** | Run your workflows on a schedule |

---

## Prerequisites

**⭐️ Important:** This lesson will involve moving between a terminal, text editor,
and jupyter notebook environment. We highly recommend using [VSCode](https://code.visualstudio.com/) for the purposes of this workshop, but you can use any combination
of tools that you're comfortable with.

> ⚠️ **Note:** Windows users need to have [WSL installed](https://docs.microsoft.com/en-us/windows/wsl/install-win10) in order to run this workshop.

- Install [Python >= 3.8](https://www.python.org/downloads/)
- Install [Docker Desktop](https://docs.docker.com/get-docker/) and make sure the Docker daemon is running.
- Install `flytectl`:

   ```bash
   # Homebrew (MacOS)
   brew install flyteorg/homebrew-tap/flytectl

   # Or Curl
   curl -sL https://ctl.flyte.org/install | sudo bash -s -- -b /usr/local/bin
   ```

---

## Setup

Create a fork of this repo by going to the
[repo link](https://github.com/flyteorg/flyte-conference-talks) and clicking
on the **Fork** button on the top right of the page. Select your username as
the repo fork owner. This will result in a repository called
`https://github.com/<username>/flyte-conference-talks`, where `<username>` is your username.

Clone your fork of the repo (replace `<username>` with your actual username):

```bash
git clone https://github.com/flyteorg/flyte-school
cd flyte-conference-talks/00-intro
```

Create a virtual environment:

```bash
python -m venv ~/venvs/flyte-school-00
source ~/venvs/flyte-school-00/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt flytekitplugins-envd jupyter
```

Test the virtual environment with:

```bash
pyflyte run \
    workflows/example_intro.py training_workflow \
    --hyperparameters '{"C": 0.01}'
```

### Start a local Flyte sandbox:

> ℹ **Note**: Before you start the local cluster, make sure that you allocate a minimum of 4 CPUs and 3 GB of memory in your Docker daemon. If you’re using the **Docker Desktop** application, you can do this easily by going to:
>
> `Settings > Resources > Advanced`
>
> Then set the CPUs and Memory sliders to the appropriate levels.


```bash
flytectl demo start
export FLYTECTL_CONFIG=~/.flyte/config-sandbox.yaml

# update task resources
flytectl update task-resource-attribute --attrFile cra.yaml
```

> ℹ **Note**: Go to the [Troubleshooting](#troubleshooting) section if you're
> having trouble getting the sandbox to start.

Test the Flyte sandbox with:

```bash
export IMAGE=ghcr.io/unionai-oss/flyte-school:00-intro-latest

pyflyte run --remote \
    --image $IMAGE \
    workflows/example_intro.py training_workflow \
    --hyperparameters '{"C": 0.01}'
```

## Tests

Install dev dependencies:

```bash
pip install pytest pytest-xdist
source ~/venvs/flyte-school-00/bin/activate
```

### Unit tests:

```bash
pytest tests/unit
```

### End-to-end tests:

First register all the workflows:

```bash
pyflyte register --image $IMAGE workflows
```

Then run the end-to-end pytest suite:

```bash
pytest tests/integration
```

> ℹ **Note**: Running the full integration test suite will take about 20 minutes.
> You can parallelize the test runner with by supplying the `pytest ... -n auto` flag.

#### Getting Help

🙌 Join the [flyte slack "ask the community" channel](https://flyte-org.slack.com/archives/CP2HDHKE1)
to get help with anything from setup to troubleshooting.


## Troubleshooting

### `Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?.`

You may need to allow the default Docker socket to be used by third-party clients.
Enable this by going to the **Docker Desktop** application and navigating to:

`Settings > Advanced`

Then, click on the checkbox next to **Allow the default Docker socket to be used**,
then **Apply & restart**.

### `OOM Killed` error

In this case you may need to free up some memory by removing unused containers
with `docker system prune -a --volumes`.
