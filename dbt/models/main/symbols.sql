{{ config(materialized='table') }}

WITH source_data AS (

    SELECT symbol
         , display_name
         , display_order
         , exchange_is_open
         , exchange_name
         , intraday_interval_minutes
         , is_trading_suspended
         , market
         , market_display_name
         , pip
         , quoted_currency_symbol
         , spot
         , spot_age
         , spot_percentage_change
         , spot_time
         , subgroup
         , subgroup_display_name
         , submarket
         , submarket_display_name
         , COALESCE(NULLIF(symbol_type,''), 'other') AS symbol_type
      FROM staging.symbols
)

SELECT *
FROM source_data
