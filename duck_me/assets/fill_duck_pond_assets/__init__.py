import pandas as pd
import duckdb 
import uuid 
from io import BytesIO

from ...partitions import daily_dump_partition          
from ...configs import S3Config, DuckPondConfig
from ...resources import S3, DuckPondHose


from dagster import (
    multi_asset, 
    asset,
    AssetIn,
    AssetOut,
    get_dagster_logger,
)

@multi_asset(outs={"sessions_df":AssetOut(), "pageviews_df":AssetOut()}, partitions_def=daily_dump_partition)
def get_swamp_water(context, config: S3Config, s3: S3):
    assert config.Bucket 
    assert config.Key
    assert s3
    logger = get_dagster_logger()
    swamp_key = config.Key + '-' + context.partition_key + '.parquet'
    ga_dump_df = pd.read_parquet(BytesIO(s3.get_file_contents(Bucket=config.Bucket, Key=swamp_key).read()), engine='pyarrow')
    session_cols = ['channel_grouping','session_date','user_id','session_id','session_sequence_number','session_start_time','session_browser','session_os','session_is_mobile','session_device_category','session_country','session_city','session_region','session_source','session_medium','session_revenue','session_total_revenue','session_order_cnt','session_pageview_cnt','session_time_on_site','new_vs_returning','session_landing_screen','session_exit_screen']
    pageview_cols = ['user_id','session_id','session_start_time','session_pageviews']
    sessions_df = ga_dump_df[session_cols]
    pageviews_df = ga_dump_df[pageview_cols]
    logger.info(f"Sessions DF Shape: {sessions_df.shape}")
    logger.info(f"Session Pageviews DF Shape: {pageviews_df.shape}")
    return sessions_df, pageviews_df

@asset(key="pond_sessions", ins={"sessions_df":AssetIn("sessions_df")}, partitions_def=daily_dump_partition)
def fill_pond_sessions(sessions_df, config: DuckPondConfig, pond_hose: DuckPondHose):
    assert config.table_name
    assert pond_hose
    logger = get_dagster_logger()
    table_name = config.table_name
    data = sessions_df.to_dict(orient='records')
    results = pond_hose.fill_duck_pond(data, table_name)
    logger.info(results)


@asset(key="pond_pageviews", ins={"pageviews_df":AssetIn("pageviews_df")}, partitions_def=daily_dump_partition)
def fill_pond_pageviews(pageviews_df, config: DuckPondConfig, pond_hose: DuckPondHose):
    assert config.table_name
    assert pond_hose 
    logger = get_dagster_logger()

    db = duckdb.connect(database=':memory:', read_only=False)
    db.register('session_pvs', pageviews_df)
    qry = """
        SELECT 
            sp.user_id,
            sp.session_id,
            sp.session_start_time,
            pv.pageview_timestamp,
            pv.hostname,
            pv.pagePath,
            pv.pageTitle,
            pv.pagePathLevel1,
            pv.pagePathLevel2,
            pv.pagePathLevel3,
            pv.pagePathLevel4,
            pv.total_product_impressions
        FROM session_pvs AS sp,
            UNNEST(session_pageviews) AS t(pv)
    """
    pageviews_df = db.query(qry).df() 
    logger.info(f"Pageviews DF Shape: {pageviews_df.shape}")
    db.close()
    pageviews_df['pageview_id'] = [uuid.uuid4().hex for _ in range(pageviews_df.shape[0])]
    data = pageviews_df.to_dict(orient='records')
    table_name = config.table_name
    results = pond_hose.fill_duck_pond(data, table_name)
    logger.info(results)




