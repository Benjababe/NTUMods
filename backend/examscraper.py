import os
import datetime
import django
import requests
import re

from bs4 import BeautifulSoup
from typing import cast

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ntumods.settings')
django.setup()

from course_module.models import Exam, Module


EXAM_SEMSTER_PAGE = "https://wis.ntu.edu.sg/webexe/owa/exam_timetable_und.MainSubmit"
EXAM_TIMETABLE_PAGE = "https://wis.ntu.edu.sg/webexe/owa/exam_timetable_und.Get_detail"

OPT_GENERAL = 1
OPT_STUDENT = 2

session = requests.Session()


class Semester:
    year: str
    num: str
    plan_no: str

    def __init__(self, year: str, num: str, plan_no: str):
        self.year = year
        self.num = num
        self.plan_no = plan_no


def get_latest_sem() -> Semester:
    global session

    res = session.post(EXAM_SEMSTER_PAGE, {
        "p_opt": OPT_GENERAL,
        "p_type": "UE",
        "bOption": "Next"
    })

    soup = BeautifulSoup(res.text, "html.parser")
    latest_semester = soup.find_all("input", {"name": "p_plan_no"})[-1]

    semester_name = latest_semester.next.strip()
    regex_res = cast(re.Match,
                     re.search(r"^AY(\d+)-\d+\sSEM\s(\d+)$", semester_name))

    return Semester(regex_res.group(1), regex_res.group(2), latest_semester["value"])


def get_exams(semester: Semester):
    res = session.post(EXAM_TIMETABLE_PAGE, {
        "p_exam_dt": "",
        "p_start_time": "",
        "p_dept": "",
        "p_subj": "",
        "p_venue": "",
        "p_matric": "",
        "academic_session": "",
        "p_plan_no": semester.plan_no,
        "p_exam_yr": semester.year,
        "p_semester": semester.num,
        "p_type": "UE",
        "bOption": "Next"
    })

    exams = process_exams(res.text)
    return exams


def process_exams(html: str):
    exams = {}
    soup = BeautifulSoup(html, "html.parser")
    exam_rows = soup.find_all("tr", {"align": "yes"})

    # exam rows: date / day / time / course code / course title / duration
    for exam_row in exam_rows:
        exam_details = exam_row.find_all("td")

        if len(exam_details) == 0:
            continue

        date = exam_details[0].text.strip()
        day = exam_details[1].text.strip()
        time = exam_details[2].text.strip()
        course_code = exam_details[3].text.strip()
        course_title = exam_details[4].text.strip()
        duration = exam_details[5].text.strip()

        exams[course_code] = {
            "date": date,
            "day": day,
            "time": time,
            "duration": duration,
        }

    return exams


def insert_exams(semester: Semester, exams: dict):
    for module_code, details in exams.items():
        # search for related module
        try:
            module_obj = Module.objects.get(code=module_code)
        except Module.DoesNotExist:
            continue

        # check if the exam is already recorded for said module
        try:
            module_obj.exam.get(semester=semester.num, year=semester.year)
            print(f"Module {module_code} has exams!")
        except Exam.MultipleObjectsReturned:
            print(f"Module {module_code} has exams!")

        # if exam isn't recorded, insert it and update the module object
        except (Exam.DoesNotExist):
            date = datetime.datetime.strptime(details["date"], "%d %B %Y")

            exam_instance = Exam(
                date=date.strftime("%Y-%m-%d"),
                time=details["time"],
                duration=details["duration"],
                semester=semester.num,
                year=semester.year
            )
            exam_instance.save()
            module_obj.exam.add(exam_instance)
            module_obj.save()

def scrape():
    semester = get_latest_sem()
    exams = get_exams(semester)
    insert_exams(semester, exams)


if __name__ == "__main__":
    scrape()
