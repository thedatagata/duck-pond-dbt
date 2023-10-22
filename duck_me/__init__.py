from .assets import load_source_data_assets
from .environment import local_S3 
from .resources import S3, DuckPondHose 
from .schedules import fill_duck_pond_schedule 

from dagster import Definitions, load_assets_from_modules

defs = Definitions(
    assets=[*load_source_data_assets], 
    resources={
        "s3": S3(access_key=local_S3['access_key'], secret_key=local_S3['secret_key'], endpoint_url=local_S3['endpoint_url']),
        "pond_hose": DuckPondHose(pipeline_name='fill_duck_pond', dataset_name='pond_water')
    },
    schedules=[fill_duck_pond_schedule]
)