import os
import psycopg2

from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path("./.env"))


def get_connect_params():
    return {
        "database": os.getenv("PG_DB"),
        "user": os.getenv("PG_USER"),
        "password": os.getenv("PG_PASSWORD"),
        "host": os.getenv("PG_HOST"),
        "port": os.getenv("PG_PORT"),
    }


def run_query(query: str):
    params = get_connect_params()
    conn = psycopg2.connect(**params)

    with conn:
        with conn.cursor() as cur:
            cur.execute(query)


def setup_semester(semester: str):
    schema_ddl = f"CREATE SCHEMA IF NOT EXISTS \"{semester}\";"
    run_query(schema_ddl)

    module_ddl = f'''
        CREATE TABLE IF NOT EXISTS "{semester}"."module" (
            module_id INT GENERATED ALWAYS AS IDENTITY,
            code VARCHAR(10) NOT NULL,
            name VARCHAR(100) NOT NULL,
            PRIMARY KEY ("module_id")
        );
    '''
    run_query(module_ddl)

    course_ddl = f'''
        CREATE TABLE IF NOT EXISTS "{semester}"."course" (
            course_id INT GENERATED ALWAYS AS IDENTITY,
            code VARCHAR(10) NOT NULL,
            sub_code VARCHAR(10) NOT NULL,
            year VARCHAR(4) NOT NULL,
            name VARCHAR(100) NOT NULL,
            type VARCHAR(4) NOT NULL,
            PRIMARY KEY ("course_id")
        );
    '''
    run_query(course_ddl)


def insert_courses(semester: str, courses: list[dict]):
    if len(courses) == 0:
        return

    course_insert_vals = []

    for course in courses:
        c_code, c_sub_code, c_year, c_type = course["code"].strip().split(";")
        c_name = course["name"]

        course_insert_vals.append(
            f'''('{c_code}','{c_sub_code}','{c_year}','{c_name}','{c_type}')'''
        )

    insert_course_dml = f'''
        INSERT INTO "{semester}"."course"
        (code, sub_code, year, name, type)
        VALUES {",".join(course_insert_vals)};
    '''
    run_query(insert_course_dml)
