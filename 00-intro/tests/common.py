"""Common testing utilities"""

from typing import Any, Dict, NamedTuple, Tuple, Type, Union

from sklearn.linear_model import LogisticRegression

from flytekit.core.workflow import PythonFunctionWorkflow
from workflows import example_intro


class WorkflowCase(NamedTuple):
    workflow: PythonFunctionWorkflow
    inputs: Dict[str, Any]
    expected_output_types: Union[Type, Tuple[Type, ...]]


WORKFLOW_CASES = [
    WorkflowCase(
        workflow=example_intro.training_workflow,
        inputs={"hyperparameters": example_intro.Hyperparameters(C=0.1, max_iter=5000)},
        expected_output_types=(LogisticRegression, float, float),
    ),
]
