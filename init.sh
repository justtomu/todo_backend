# install dependencies & prepare db & run tests
pipenv install
flask db upgrade
python -m unittest discover tests
