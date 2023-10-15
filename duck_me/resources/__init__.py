import dlt
from pathlib import Path
import boto3
import duckdb
from dagster import ConfigurableResource  

# db_path = Path(__file__).parent.parent.parent / 'data_warehouse' / 'duck_pond.db'

from dagster import (
    ConfigurableResource,
)

class DuckPondHose(ConfigurableResource):
    pipeline_name: str
    dataset_name: str
    
    def fill_duck_pond(self, data, table_name):
        pipeline = dlt.pipeline(pipeline_name=self.pipeline_name, destination='duckdb', dataset_name=self.dataset_name, credentials='data_warehouse/duck_pond.duckdb')
        info = pipeline.run(data, table_name=table_name, loader_file_format='parquet')
        return info
        
class S3(ConfigurableResource):
    access_key: str
    secret_key: str
    endpoint_url: str

    def get_client(self):
        return boto3.session.Session().client(
            service_name='s3',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            endpoint_url=self.endpoint_url,
            verify=False
        )
    
    def get_file_contents(self, Bucket, Key):
        s3_client = self.get_client()
        return s3_client.get_object(Bucket=Bucket, Key=Key).get('Body')



