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
         , CAST(close AS NUMERIC) AS close
         , CAST(high AS NUMERIC) AS high
         , CAST(low AS NUMERIC) AS low
         , CAST(open AS NUMERIC) AS open
         , DATE(TIMESTAMP_SECONDS(time)) AS date
      FROM staging.candles_history
)

SELECT *
FROM source_data
