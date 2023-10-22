from ..assets import load_source_data_assets
from ..partitions import daily_dump_partition

from dagster import define_asset_job

fill_pond_config = {
    "execution": {
        "config": {
            "multiprocess":{
                "max_concurrent": 1
            }
        }
    },
    "ops":{
        "get_swamp_water":{"config":{"Bucket":"data-swamp","Key":"ga_data"}},
        "pond_sessions":{"config":{"table_name":"raw_sessions_fct"}},
        "pond_pageviews":{"config":{"table_name":"raw_pageviews_fct"}}
    }
}

fill_duck_pond_job = define_asset_job(
    "fill_duck_pond", 
    selection=[*load_source_data_assets], 
    config=fill_pond_config,
    partitions_def=daily_dump_partition,
)