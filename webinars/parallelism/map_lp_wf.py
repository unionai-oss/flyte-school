import union
from union import task, workflow, dynamic, ImageSpec, map_task
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler


custom_image = ImageSpec(
    builder="union",
    packages=["pandas",
              "scikit-learn",
              "pyarrow",],
)

actor = union.ActorEnvironment(
    name="my-actor",
    replica_count=3,
    ttl_seconds=30,
    requests=union.Resources(
        cpu="2",
        mem="300Mi",
    ),
    container_image=custom_image,
)

@union.task(container_image=custom_image)
def preprocess_data() -> pd.DataFrame:
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
    column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']
    iris = pd.read_csv(url, header=None, names=column_names)
    iris['species'] = iris['species'].astype('category').cat.codes
    X = iris.drop('species', axis=1)
    y = iris['species']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    processed_data = pd.DataFrame(X_scaled, columns=X.columns)
    processed_data['species'] = y
    return processed_data

@actor.task
def train_model(data: pd.DataFrame, hyperparameter: float) -> float:
    X = data.drop('species', axis=1)
    y = data['species']
    model = LogisticRegression(C=hyperparameter)
    model.fit(X, y)
    predictions = model.predict(X)
    accuracy = accuracy_score(y, predictions)
    return accuracy

@union.workflow
def subworkflow(hyperparameter: float) -> float:
    data = preprocess_data()
    accuracy = train_model(data=data, hyperparameter=hyperparameter)
    return accuracy

# Create a launch plan for the subworkflow
subworkflow_lp = union.LaunchPlan.get_or_create(
    workflow=subworkflow,
    name="subworkflow_launch_plan",
)

@union.workflow
def ml_pipeline(hyperparameters: list[float]) -> list[float]:
    # Map over the launch plans with different hyperparameters
    return union.map(subworkflow_lp)(hyperparameter=hyperparameters)

@union.workflow
def mplp_ml_pipeline() -> list[float]:
    # Map over the launch plans with different hyperparameters
    hyperparameters = [x/10.0 for x in range(5,5000,10)]
    return union.map(subworkflow_lp)(hyperparameter=hyperparameters)