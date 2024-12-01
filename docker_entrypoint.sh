# install dependencies & prepare db & run tests
flask db upgrade
python -m unittest discover tests

python wsgi.py