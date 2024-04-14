FROM python:3.12-slim

# Install required system packages and cleanup to reduce image size
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends git libpq-dev && \
    pip install --no-cache-dir --upgrade pip dbt-bigquery==1.7.7  && \
#   git libpq-dev python-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set working directory
ENV DBT_DIR /dbt/
WORKDIR $DBT_DIR

# Copy files to the image
COPY . $DBT_DIR

# Run dbt
ENTRYPOINT ["dbt"]
