# deriv-market-datahub


- server status
- active symbols
filter on "market": "indices",

- active symbols and their last quote in a day
- get historical last 30 days quotes for a symbol -> store in table
- daily job to get yesterday last tick for all active symbols

- load data to GCS
- terraform GCS + service account + key
- terraform cloud composer
- dag to load data from GCS to BQ


## Plan

- Call deriv API to load data into GCS
- Spin up airflow using terraform
- Call this extraction from airflow
- Load data into BQ using airflow operator
- Create BQ schema
- Use DBT to create a model on top of BQ table
- Create a dashboard in data studio
