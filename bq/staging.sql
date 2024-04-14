CREATE OR REPLACE DATASET `<YOUR_PROJECT_ID>.staging`;

CREATE EXTERNAL TABLE `staging.symbols`
OPTIONS(
  format="PARQUET",
  uris=[""gs://staging-market-datahub/market_data/symbols/*.parquet""]
);

CREATE EXTERNAL TABLE `staging.countries`
OPTIONS(
  format="PARQUET",
  uris=[""gs://staging-market-datahub/market_data/countries/*.parquet""]
);

CREATE EXTERNAL TABLE `staging.countries__tin_format`
OPTIONS(
  format="PARQUET",
  uris=[""gs://staging-market-datahub/market_data/countries__tin_format/*.parquet""]
);

CREATE EXTERNAL TABLE `staging.candles_history`
OPTIONS(
  format="PARQUET",
  uris=[""gs://staging-market-datahub/market_data/candles_history/*.parquet""]
);

CREATE EXTERNAL TABLE `staging.ticks_history`
OPTIONS(
  format="PARQUET",
  uris=[""gs://staging-market-datahub/market_data/ticks_history/*.parquet""]
);

CREATE EXTERNAL TABLE `staging.assets`
OPTIONS(
  format="PARQUET",
  uris=[""gs://staging-market-datahub/market_data/assets/*.parquet""]
);

CREATE EXTERNAL TABLE `staging.assets__value`
OPTIONS(
  format="PARQUET",
  uris=[""gs://staging-market-datahub/market_data/assets__value/*.parquet""]
);

CREATE EXTERNAL TABLE `staging.assets__value__list`
OPTIONS(
  format="PARQUET",
  uris=[""gs://staging-market-datahub/market_data/assets__value__list/*.parquet""]
);
