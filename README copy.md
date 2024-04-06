# project-template


**To generate auto-documentation**:

```bash
pip3 install pdoc3
python3 -m pdoc --html --force --template-dir docs/template airflow/dags -o docs/html
```

**To make changes**:

- Setup project for the first time: `make setup`
- Then reload you session to make poetry available in your Path or to configure your current shell run `source $HOME/.poetry/env`
- Then run `make install`
- Run linter: `make tidy`
- Run test cases: `make test`

**TO update TOML file**:

- `poetry self add poetry-plugin-up` this will add option to enable update toml file
- more here: https://github.com/MousaZeidBaker/poetry-plugin-up
