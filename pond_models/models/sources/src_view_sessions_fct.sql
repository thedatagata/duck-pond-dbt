WITH 
    raw_sessions_deduped
      AS 
        (
          {{ dbt_utils.deduplicate(
            relation=source('dagster', 'pond_sessions'),
            partition_by='user_id, session_id',
            order_by="session_start_time desc",
            )
          }}
        ) 
SELECT 
    s.session_id 
  , s.session_start_time 
  , s.session_sequence_number 
  , s.user_id 
  , s.session_date 
  , s.session_pageview_cnt
  , s.session_order_cnt 
  , s.session_order_revenue 
  , s.session_total_revenue
  , s.session_new_vs_returning
  , s.session_time_on_site 
  , s.session_browser
  , s.session_os 
  , s.session_is_mobile 
  , s.session_device_category
  , s.session_source 
  , s.session_medium 
  , s.session_marketing_channel 
  , s.session_city 
  , s.session_region 
  , s.session_country
FROM raw_sessions_deduped s
