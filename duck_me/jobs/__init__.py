from ..partitions import daily_dump_partition

from dagster import define_asset_job 

fill_pond_config = {}

fill_duck_pond_job = define_asset_job("fill_duck_pond", selection=[], config=fill_pond_config, partitions_def=daily_dump_partition)