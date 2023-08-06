import json
import logging
import os
import subprocess
from pathlib import Path

import flask

import ibdb.api
from vendor.pg_dump_splitsort import split_sql_file

IBDB_URL = os.environ.get('IDDB_URL', 'ibdb://data-with-babish.jklewa.github.com/datasets')
IBDB_SQLFILE = os.environ.get('IBDB_SQLFILE', 'ibdb/db_dump.sql')
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', 'datasets/')

DB_USERNAME = os.environ.get('POSTGRES_USERNAME', 'postgres')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'postgres')
DB_NAME = os.environ.get('POSTGRES_DBNAME', 'babish_db')
DB_HOSTNAME = os.environ.get('POSTGRES_HOSTNAME', 'db')
DB_PORT = int(os.environ.get('POSTGRES_PORT', '5432'))


def write_response(route, to=None, **kwargs):
    logging.info(f'Writing {route} to {to}')
    kwargs['base_url'] = kwargs.get('base_url') or IBDB_URL
    with ibdb.api.app.test_client() as c:
        r: flask.Response = c.get(route, **kwargs)
        with open(to, 'w', encoding='utf8') as o:
            json.dump(r.json, o, indent=2)


def write_datasets():
    logging.info(f'Writing datasets to {OUTPUT_DIR}')
    write_response('/episodes?format=json', to=os.path.join(OUTPUT_DIR, 'ibdb.episodes.json'))
    write_response('/guests?format=json', to=os.path.join(OUTPUT_DIR, 'ibdb.guests.json'))
    write_response('/recipes?format=json', to=os.path.join(OUTPUT_DIR, 'ibdb.recipes.json'))
    write_response('/references?format=json', to=os.path.join(OUTPUT_DIR, 'ibdb.references.json'))
    write_response('/shows?format=json', to=os.path.join(OUTPUT_DIR, 'ibdb.shows.json'))


def cleanup_sqlfile(sql_filepath):
    base_dir = os.path.dirname(sql_filepath)
    split_sql_file(sql_filepath)
    temp_sql_files = sorted(Path(base_dir).glob('[0-9]*.sql'))
    if len(temp_sql_files) > 0:
        with open(sql_filepath, 'w') as f:
            subprocess.run(['cat', *temp_sql_files], stdout=f)
        subprocess.run(['rm', *temp_sql_files])
    else:
        logging.error('pg_dump_splitsort did not produce the files expected')


def db_dump():
    logging.info(f'Writing database to {IBDB_SQLFILE}')
    subprocess.run(f'''
        PGPASSWORD={DB_PASSWORD} PGUSER={DB_USERNAME} PGHOST={DB_HOSTNAME} PGPORT={DB_PORT} \
        pg_dump --dbname={DB_NAME} --create --file={IBDB_SQLFILE}''', shell=True)
    cleanup_sqlfile(IBDB_SQLFILE)


def export():
    write_datasets()
    db_dump()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    export()
