## Plan dashboard

- filter on "market": "indices",

- active symbols and their last quote in a day
- get historical last 30 days quotes for a symbol -> store in table
- daily job to get yesterday last tick for all active symbols

# Todo

- Create composer environment [done]
- Create service account and key to be used in GCS to load data into GCS [done]
- Update composer environment with service account key [done]
- Update composer connection with environment variables [done] (change env variables to pass docker image and replace secrets.toml)
- Create artifact registry [done]
- Add airflow connection to be used in docker operator [done]
- Test airflow dag [done]
- Clone airflow dag to multiple dags [done]
- Create a dag calling the docker image multiple times [done]
- change dag to loop over list which contains the list of symbols [so we tick/candle for each symbol] !!!!!
- Create a dag to load data from GCS to BQ
- Add BQ table schema `staging`
- Add dbt core and call it from airflow using docker operator (or just load data into BQ, using airflow operator)
- Use DBT to move data from staging to `main`  schema
- Create a dashboard in data studio
