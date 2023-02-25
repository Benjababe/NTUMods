# Pages Scraped

- [Course Information Selection](https://wis.ntu.edu.sg/webexe/owa/aus_subj_cont.main)
- [Course Schedule Information](https://wish.wis.ntu.edu.sg/webexe/owa/aus_schedule.main)
- [Exam Timetable](https://wis.ntu.edu.sg/webexe/owa/exam_timetable_und.main)

# Pre-requisites

Ensure you have a `.env` file in the same directory as `settings.py` with the following properties set

```
DEBUG=TRUE

# Secret key for generating an authentication token
SECRET_KEY=

# Name of the postgres database
DBNAME=ntumods

# Username to access the postgres database
DBUSERNAME=postgres

# Password of the user
DBPASSWORD=password
```