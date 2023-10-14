from dagster import build_schedule_from_partitioned_job 

from ..jobs import fill_duck_pond_job

fill_duck_pond_schedule = build_schedule_from_partitioned_job(fill_duck_pond_job)