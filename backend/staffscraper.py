import os
import django
import urllib.parse

import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ntumods.settings')
django.setup()

from staff.models import TeachingStaff, Appointment, Interest

FACULTY_DIR_PAGE = "https://www.ntu.edu.sg/research/faculty-directory/GetAcademicProfiles/?searchFaculty=&interests=all&page={}"

class Staff:
    def __init__(self, title, email, tag, url, profile_pic_url, desc, appointments, interests):
        self.title: str = title
        self.email: str = email
        self.tag: str = tag
        self.url: str = urllib.parse.quote(url, safe=":/?=&")
        self.profile_pic_url: str = urllib.parse.quote(profile_pic_url, safe=":/?=&")
        self.desc: str = desc
        self.appointments: list[str] = appointments
        self.interests: list[str] = interests
        


def get_all_staff() -> list[Staff]:
    all_staff = []
    page_num = 1
    total_pages = 1
    
    while page_num < total_pages + 1:
        print(f"Fetching page {page_num}/{total_pages}")
        res = requests.get(FACULTY_DIR_PAGE.format(page_num))
        page_num += 1
        
        if res.ok:
            data = res.json()
            total_pages = data["totalPages"]
            all_staff += get_staff_in_page(data["items"])
        else:
            break
        
    return all_staff
        
        
def get_staff_in_page(data: list[dict]) -> list[Staff]:
    staff = list(map(staff_dict_to_obj, data))    
    return staff
    
def staff_dict_to_obj(s_dict: dict) -> Staff:
    appointments = [] if s_dict["appointments"] is None \
        else list(map(str.strip, s_dict["appointments"].split("<br/>")))
    interests = [] if s_dict["interests"] is None \
        else list(map(str.strip, s_dict["interests"].split("|")))
    
    return Staff(
        s_dict["title"],
        s_dict["email"],
        s_dict["tag"],
        s_dict["url"],
        s_dict["profilepictureurl"],
        s_dict["description"],
        appointments,
        interests
    )
    
def insert_all_staff(all_staff: list[Staff]):
    for staff in all_staff:
        appointment_refs = get_appointment_refs(staff.appointments)
        interest_refs = get_interest_refs(staff.interests)
        
        t_staff, created = TeachingStaff.objects.get_or_create(
            title=staff.title,
            email=staff.email,
            tag=staff.tag,
            url=staff.url,
            profile_pic_url=staff.profile_pic_url,
            description=staff.desc
        )
        
        if created:
            print(f"Added {staff.title}")
        
        for appointment_ref in appointment_refs:
            t_staff.appointments.add(appointment_ref)
        for interest_ref in interest_refs:
            t_staff.interests.add(interest_ref)


def get_appointment_refs(appointments: list[str]) -> list[Appointment]:
    appointment_refs = []
    
    for appt in appointments:
        obj, created = Appointment.objects.get_or_create(name=appt)
        appointment_refs.append(obj)
        
    return appointment_refs

def get_interest_refs(interests: list[str]) -> list[Interest]:
    interest_refs = []
    
    for interest in interests:
        obj, created = Interest.objects.get_or_create(name=interest)
        interest_refs.append(obj)
        
    return interest_refs
            

def scrape():
    all_staff = get_all_staff()
    insert_all_staff(all_staff)


if __name__ == "__main__":
    scrape()