import json
import re
from typing import cast

import bs4
import requests
from bs4 import BeautifulSoup

import db

SCHEDULE_SELECT_PAGE = "https://wish.wis.ntu.edu.sg/webexe/owa/aus_schedule.main"
COURSE_DETAIL_PAGE = "https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1"
COURSE_INFO_PAGE = "https://wis.ntu.edu.sg/webexe/owa/AUS_SUBJ_CONT.main_display1"


def get_all_courses(force_semester="") -> dict:
    """
    Returns all courses for the current or given semester

    Args:
        force_semester (str, optional): Academic semester to filter, format "YYYY;S". 
        Eg. "2022;2" for 2022 Sem 2 Defaults to "".

    Returns:
        dict: Dict containing the semester and all courses in it.
    """

    res = requests.get(SCHEDULE_SELECT_PAGE)
    soup = BeautifulSoup(res.text, "html.parser")

    if force_semester == "":
        semester_selector = soup.find("select", {"name": "acadsem"})
        semester_selector = cast(bs4.element.Tag, semester_selector)

        active_semester = semester_selector.find("option", {"selected": True})
        active_semester = cast(bs4.element.Tag, active_semester)

        semester = active_semester["value"]
    else:
        semester = force_semester

    # gets the list of course selections
    course_selector = soup.find("select", {"name": "r_course_yr"})
    course_selector = cast(bs4.element.Tag, course_selector)

    # within the list, find all selectable courses
    courses = course_selector.find_all("option", {"value": True})

    # remove options with empty course values
    courses = list(filter(lambda c: c["value"] != "", courses))

    # only keep course value and name
    courses = list(map(lambda c: {
        "code": c["value"],
        "name": c.text.strip()
    }, courses))

    return {
        "semester": semester,
        "courses": courses
    }


def scrape_all_courses(schedule: dict):
    """
    Goes through all available courses and scrapes 
    the modules for the given academic semester

    Args:
        schedule (dict): Dict containing keys "semester" and "courses"
    """

    schedule["modules"] = {}
    semester = schedule["semester"]
    courses = schedule["courses"]

    for course in courses:
        course_name = course["name"]
        print(f"Scraping {course_name}")

        course_info = course["code"].split(";")
        r_search_type = course_info[-1]

        res = requests.post(COURSE_DETAIL_PAGE, {
            "acadsem": semester,
            "r_course_yr": course["code"],
            "r_subj_code": "",
            "r_search_type": r_search_type,
            "boption": "CLoad",
            "staff_access": "false",
        })

        if res.ok:
            course_modules = get_course_modules(res.text)
            append_modules(schedule, course_modules)

        else:
            print(f"Error with scraping {course_name}")
            continue

        # retrieve module description & grading types
        res = requests.post(COURSE_INFO_PAGE, {
            "acadsem": semester.replace(";", "_"),
            "r_course_yr": course["code"],
            "r_subj_code": "",
            "boption": "CLoad",
            "acad": semester.split(";")[0],
            "semester": semester.split(";")[1]
        })

        if res.ok:
            insert_module_info(schedule, res.text)


def insert_module_info(schedule: dict, html: str):
    soup = BeautifulSoup(html, "html.parser")
    module_tables = soup.find_all("table")

    for module_table in module_tables:
        rows = module_table.find_all("tr")

        header = rows[0].find_all("td")
        code = header[0].text

        if code not in schedule["modules"]:
            continue

        desc = rows[-1].find("td").text
        schedule["modules"][code]["desc"] = desc.replace("'", "")

        rows = rows[1:-1]

        for row in rows:
            cells = row.find_all("td")
            header_cell = cells[0]
            if "Grade Type" in header_cell.text:
                grading = cells[1].text
                schedule["modules"][code]["grading"] = grading
                break


def append_modules(schedule, course_modules):
    for course_module in course_modules:
        module_code = course_module["code"]

        # add timeslots if necessary
        if module_code in schedule["modules"]:
            for timeslot in course_module["timeslots"]:
                if timeslot not in schedule["modules"][module_code]["timeslots"]:
                    schedule["modules"][module_code]["timeslots"]\
                        .append(timeslot)

        else:
            schedule["modules"][module_code] = {
                "name": course_module["name"],
                "timeslots": course_module["timeslots"],
                "credits": course_module["credits"],
                "desc": "",
                "grading": ""
            }


def get_course_modules(course_page_text: str) -> list[dict]:
    """
    Parses the course page with all the modules and returns a list 
    of modules for the course in the given academic semester

    Args:
        course_page_text (str): Text response from course detail POST request

    Returns:
        List[dict]: List of modules for the course in the given academic semester
    """

    modules = []

    soup = BeautifulSoup(course_page_text, "html.parser")
    tbl_headers = soup.find_all("table", {"border": False})

    # each tbl_header represents a module
    for tbl_header in tbl_headers:
        header_cells = tbl_header.find("tr").find_all("td")
        module_code = header_cells[0].text
        module_name = header_cells[1].text

        res = cast(re.Match[str], re.search(
            r"(\d*.\d)\s+AU", header_cells[2].text))
        module_credits = res.group(1)

        module = {
            "code": module_code,
            "name": module_name,
            "credits": module_credits,
            "timeslots": [],
        }

        time_table = tbl_header.find_next_sibling()
        time_slots = time_table.find_all("tr")
        slot_index = "-1"

        for time_slot in time_slots:
            time_slot_cells = time_slot.find_all("td")
            time_slot_cells = list(
                map(lambda c: c.text.strip(), time_slot_cells)
            )

            if len(time_slot_cells) == 0:
                continue

            # if index is empty, use the previous stored one
            if time_slot_cells[0] != "":
                slot_index = time_slot_cells[0]

            # split the array, skipping the index
            slot_type, slot_group, slot_day, \
                slot_time, slot_venue, slot_remark = time_slot_cells[1:]

            module["timeslots"].append({
                "index": slot_index,
                "type": slot_type,
                "group": slot_group,
                "day": slot_day,
                "time": slot_time,
                "venue": slot_venue,
                "remark": slot_remark,
            })

        modules.append(module)

    return modules


def scrape():
    courses = get_all_courses()
    db.insert_courses(courses["courses"])

    scrape_all_courses(courses)
    db.insert_modules(courses["modules"])


if __name__ == "__main__":
    scrape()
