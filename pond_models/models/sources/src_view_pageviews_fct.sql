WITH 
    raw_page_views_deduped
        AS (
            {{ dbt_utils.deduplicate(
                relation=source('dagster', 'pond_pageviews'),
                partition_by='user_id, pageview_id',
                order_by="pageview_timestamp desc",
            )
            }}
        )
SELECT
    p.pageview_id 
  , p.pageview_timestamp
  , p.user_id
  , p.session_id 
  , p.session_start_time 
  , p.pageview_page_title 
  , p.pageview_host 
  , p.pageview_path 
  , p.pageview
  , p.pageview_path_part_1 
  , p.pageview_path_part_2
  , p.pageview_path_part_3
  , p.pageview_path_part_4 
  , p.pageview_product_impressions
FROM raw_page_views_deduped p
