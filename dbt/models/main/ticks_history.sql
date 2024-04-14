{{ config(
    materialized='table',
    cluster_by = "symbol",
    partition_by={
      "field": "date",
      "data_type": "date",
      "granularity": "month"
    },
) }}

WITH source_data AS (

    SELECT ticks_history AS symbol
         , style
         , pip_size
         , CAST(price AS NUMERIC) AS price
         , DATE(TIMESTAMP_SECONDS(time)) AS date
      FROM staging.ticks_history
)

SELECT *
FROM source_data
