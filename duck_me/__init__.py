import os
from .assets import load_source_data_assets 
from .assets.pond_model_assets import pond_model_assets
from .constants import local_S3, dbt_project_dir
from .resources import S3, DuckPondHose 
from .schedules import fill_duck_pond_schedule 

from dagster import Definitions
from dagster_dbt import DbtCliResource

dbt_project_path = os.fspath(dbt_project_dir)

defs = Definitions(
    assets=[*load_source_data_assets, pond_model_assets], 
    resources={
        "s3": S3(access_key=local_S3['access_key'], secret_key=local_S3['secret_key'], endpoint_url=local_S3['endpoint_url']),
        "pond_hose": DuckPondHose(pipeline_name='fill_duck_pond', dataset_name='pond_water'),
        "dbt": DbtCliResource(project_dir=dbt_project_dir)
    },
    schedules=[fill_duck_pond_schedule]
)