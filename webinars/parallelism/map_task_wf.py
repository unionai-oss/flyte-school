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

@task(container_image=custom_image)
def preprocess_data() -> pd.DataFrame:
    # Load the Iris dataset from a URL
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
    column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']
    iris = pd.read_csv(url, header=None, names=column_names)

    # Preprocess the data
    # Convert species to a numerical value
    iris['species'] = iris['species'].astype('category').cat.codes

    # Split the data into features and labels
    X = iris.drop('species', axis=1)
    y = iris['species']

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Combine the features and labels back into a DataFrame
    processed_data = pd.DataFrame(X_scaled, columns=X.columns)
    processed_data['species'] = y

    return processed_data

@task(container_image=custom_image)
def train_model(data: pd.DataFrame, hyperparameter: float) -> float:
    # Split data into features and labels

    X = data.drop('species', axis=1)
    y = data['species']

    # Train a simple logistic regression model
    model = LogisticRegression(C=hyperparameter)
    model.fit(X, y)

    # Predict and calculate accuracy
    predictions = model.predict(X)
    accuracy = accuracy_score(y, predictions)
    return accuracy


@dynamic(container_image=custom_image)
def dynamic_workflow(hyperparameters: list[float]) -> list[float]:
    # Preprocess data
    data = preprocess_data()
    # Use map_task to train models in parallel with different hyperparameters
    accuracies = map_task(train_model)(data=[data] * len(hyperparameters), hyperparameter=hyperparameters)

    return accuracies

@workflow
def ml_pipeline(hyperparameters: list[float]) -> list[float]:
    return dynamic_workflow(hyperparameters=hyperparameters)

@workflow
def map_ml_pipeline() -> list[float]:
    hyperparameters = [x/10.0 for x in range(5,5000,10)]
    return dynamic_workflow(hyperparameters=hyperparameters)