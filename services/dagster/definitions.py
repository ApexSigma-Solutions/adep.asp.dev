from dagster import Definitions, asset

@asset
def example_asset():
    """A simple example asset for Dagster."""
    return "Hello, ApexSigma!"

defs = Definitions(
    assets=[example_asset],
)