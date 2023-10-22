{{ dbt_utils.deduplicate(
    relation=source('pond_water', 'raw_pageviews_fct'),
    partition_by='user_id, pageview_id',
    order_by="pageview_timestamp desc",
   )
}}