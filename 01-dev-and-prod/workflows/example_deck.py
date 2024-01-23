import flytekit
from flytekit import ImageSpec, task
from flytekitplugins.deck.renderer import MarkdownRenderer
from sklearn.decomposition import PCA

custom_image = ImageSpec(
    name="flyte-decks-example", packages=["plotly"], registry="localhost:30000"
)

if custom_image.is_container():
    import plotly
    import plotly.express as px


@task(enable_deck=True, container_image=custom_image)
def pca_plot():
    iris_df = px.data.iris()
    X = iris_df[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
    pca = PCA(n_components=3)
    components = pca.fit_transform(X)
    total_var = pca.explained_variance_ratio_.sum() * 100
    fig = px.scatter_3d(
        components,
        x=0,
        y=1,
        z=2,
        color=iris_df["species"],
        title=f"Total Explained Variance: {total_var:.2f}%",
        labels={"0": "PC 1", "1": "PC 2", "2": "PC 3"},
    )
    main_deck = flytekit.Deck(
        "pca", MarkdownRenderer().to_html("### Principal Component Analysis")
    )
    main_deck.append(plotly.io.to_html(fig))
