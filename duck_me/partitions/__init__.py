from dagster import DailyPartitionsDefinition 

daily_dump_partition = DailyPartitionsDefinition(start_date="2023-10-21", end_date="2023-10-23")