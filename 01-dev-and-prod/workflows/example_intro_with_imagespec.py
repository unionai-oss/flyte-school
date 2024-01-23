"""Flyte Intro: Tasks and Workflows.

These examples will use the penguins dataset:
https://allisonhorst.github.io/palmerpenguins/

Using the pypi package:
https://pypi.org/project/palmerpenguins/
"""

from dataclasses import dataclass, asdict
from typing import Optional, Tuple

import pandas as pd
from dataclasses_json import dataclass_json


from flytekit import task, workflow, LaunchPlan, CronSchedule, ImageSpec

try:
    from workflows import logger
except:
    pass

custom_image = ImageSpec(
    name="dev-and-prod",
    registry="localhost:30000",
    packages=["palmerpenguins", "scikit-learn"],
)


TARGET = "species"
FEATURES = [
    "bill_length_mm",
    "bill_depth_mm",
    "flipper_length_mm",
    "body_mass_g",
]


@dataclass_json
@dataclass
class Hyperparameters:
    C: float
    max_iter: Optional[int] = 2500


if custom_image.is_container():
    from palmerpenguins import load_penguins
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression

    @task(container_image=custom_image)
    def get_data() -> pd.DataFrame:
        return load_penguins()[[TARGET] + FEATURES].dropna()

    @task(container_image=custom_image)
    def split_data(
        data: pd.DataFrame, test_size: float, random_state: int
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return train_test_split(
            data,
            test_size=test_size,
            random_state=random_state,
        )

    @task(container_image=custom_image)
    def train_model(
        data: pd.DataFrame,
        hyperparameters: Hyperparameters,
    ) -> LogisticRegression:
        return LogisticRegression(**asdict(hyperparameters)).fit(
            data[FEATURES], data[TARGET]
        )

    @task(container_image=custom_image)
    def evaluate(model: LogisticRegression, data: pd.DataFrame) -> float:
        return float(accuracy_score(data[TARGET], model.predict(data[FEATURES])))

    @workflow
    def training_workflow(
        hyperparameters: Hyperparameters,
        test_size: float = 0.2,
        random_state: int = 42,
    ) -> Tuple[LogisticRegression, float, float]:
        # get and split data
        data = get_data()
        train_data, test_data = split_data(
            data=data, test_size=test_size, random_state=random_state
        )

        # train model on the training set
        model = train_model(data=train_data, hyperparameters=hyperparameters)

        # evaluate the model
        train_acc = evaluate(model=model, data=train_data)
        test_acc = evaluate(model=model, data=test_data)

        # return model with results
        return model, train_acc, test_acc
