import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

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

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
    except Exception as ex:
        print(ex)


def run_query_return(query: str) -> list[tuple[int]]:
    params = get_connect_params()
    conn = psycopg2.connect(**params)

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()
    except Exception as ex:
        print(ex)

    return []


def insert_courses(courses: list[dict]):
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
        INSERT INTO "public"."course_module_course"
        (code, sub_code, year, name, type)
        VALUES {",".join(course_insert_vals)}
        ON CONFLICT ('code', 'sub_code', 'year', 'type')
        DO NOTHING
    '''
    run_query(insert_course_dml)


def insert_modules(modules: dict, semester: str, year: str):
    if len(modules) == 0:
        return

    module_insert_vals = []
    timeslot_insert_vals = []
    venue_insert_vals = set()

    for module_code, module in modules.items():
        timeslots = module["timeslots"]

        module_name = module["name"].replace("'", "")
        module_insert_vals.append(
            f'''(
                '{module_code}', 
                '{module_name}', 
                '{module["credits"]}', 
                '{module["desc"]}', 
                '{module["grading"]}'
            )'''
        )

        for timeslot in timeslots:
            if "-" in timeslot["time"]:
                t_start, t_end = map(
                    lambda t: f"'{t}'", timeslot["time"].split("-")
                )
            else:
                t_start, t_end = "NULL", "NULL"

            venue = timeslot["venue"]
            venue = venue.replace("/", "")
            venue_insert_vals.add(f"('{venue}')")

            timeslot_insert_vals.append(
                f'''(
                    '{timeslot["type"]}',
                    '{timeslot["group"]}',
                    '{timeslot["day"]}',
                    {t_start},
                    {t_end},
                    '{timeslot["remark"]}',
                    '{semester}',
                    '{year}',
                    '{timeslot["index"]}',
                    '{module_code}',
                    (SELECT id FROM "public"."venue_venue" WHERE name='{venue}')
                )''')

    module_insert_dml = f'''
        INSERT INTO "public"."course_module_module"
        (code, "name", credits, "desc", grading)
        VALUES {",".join(module_insert_vals)}
        ON CONFLICT (code)
        DO NOTHING
    '''
    run_query(module_insert_dml)

    venue_insert_dml = f'''
        INSERT INTO "public"."venue_venue"
        (name)
        VALUES{",".join(list(venue_insert_vals))}
        ON CONFLICT (name)
        DO NOTHING
    '''
    run_query(venue_insert_dml)

    timeslot_insert_dml = f'''
        INSERT INTO "public"."timeslot_timeslot"
        (type, "group", day, time_start, time_end, remarks, semester, year, index, module_id, venue_id)
        VALUES{",".join(timeslot_insert_vals)}
        ON CONFLICT (index, "group", day, time_start, time_end, semester, year, module_id)
        DO NOTHING
    '''
    run_query(timeslot_insert_dml)


def insert_exams(exams: dict, semester: str, year: str):
    exam_insert_vals = []

    for module_code, exam_details in exams.items():
        exam_insert_vals.append(f'''(
            '{exam_details["date"]}',
            '{exam_details["time"]}',
            '{exam_details["duration"]}',
            '{semester}',
            '{year}'
        )''')

    exam_insert_dml = f'''
        INSERT INTO "public"."course_module_exam"
        (date, time, duration, semester, year)
        VALUES{",".join(exam_insert_vals)}
    '''
    run_query(exam_insert_dml)
