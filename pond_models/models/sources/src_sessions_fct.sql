{{ dbt_utils.deduplicate(
    relation=source('pond_water', 'raw_sessions_fct'),
    partition_by='user_id, session_id',
    order_by="session_start_time desc",
   )
}}