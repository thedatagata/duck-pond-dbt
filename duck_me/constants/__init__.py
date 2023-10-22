from pathlib import Path

dbt_project_dir = Path(__file__).joinpath("..","..", "..", "pond_models").resolve()
dbt_manifest_path = dbt_project_dir.joinpath("target","manifest.json")
data_warehouse_dir = Path(__file__).joinpath("..", "..", "data_warehouse").resolve()
duck_pond_path = data_warehouse_dir.joinpath("duckpond.db")

local_S3 = {
    "access_key": "test",
    "secret_key": "test",
    "endpoint_url": "http://localhost:4566"
}