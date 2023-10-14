from dagster import Config 

class DuckPondConfig(Config):
    table_name: str

class S3Config(Config):
    Bucket: str
    Key: str