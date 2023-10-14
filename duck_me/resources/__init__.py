import dlt
from pathlib import Path
import boto3
from dagster import ConfigurableResource  

db_path = Path(__file__).parent.parent.parent / 'data_warehouse' / 'duck_pond.db'

from dagster import (
    ConfigurableResource,
)

class DuckPondHose(ConfigurableResource):
    pipeline_name: str
    dataset_name: str 

    def get_pond_hose(self):
        return dlt.pipeline(pipeline_name=self.pipeline_name, destination='duckdb', dataset_name=self.dataset_name, credentials=db_path) 
    
    def fill_duck_pond(self, table_name, data):
        pond_hose = self.get_pond_hose()
        return pond_hose.run(table_name, data)
        
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



