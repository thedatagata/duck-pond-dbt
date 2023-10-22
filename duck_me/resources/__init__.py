from ..constants import duck_pond_path
import dlt
import boto3
import duckdb
from dagster import ConfigurableResource  

from dagster import (
    ConfigurableResource,
)

class DuckPondHose(ConfigurableResource):
    pipeline_name: str
    dataset_name: str

    def get_duckpond_conn(self):
        return duckdb.connect(database='data_warehouse/duckpond.db', read_only=False)
    
    def fill_duck_pond(self, data, table_name):
        duckpond_db = self.get_duckpond_conn()
        pipeline = dlt.pipeline(pipeline_name=self.pipeline_name, destination='duckdb', dataset_name=self.dataset_name, credentials=duckpond_db)
        info = pipeline.run(data, table_name=table_name, loader_file_format='parquet')
        duckpond_db.close()
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



