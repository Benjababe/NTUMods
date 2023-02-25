import db
import modscraper


def main():
    populate_courses("2022;2")


def populate_courses(semester: str):
    programmes = modscraper.get_all_courses(force_semester=semester)
    db.setup_semester(semester)
    db.insert_courses(programmes["semester"], programmes["courses"])


if __name__ == "__main__":
    main()
