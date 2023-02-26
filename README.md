# Pages Scraped

- [Course Information Selection](https://wis.ntu.edu.sg/webexe/owa/aus_subj_cont.main)
- [Course Schedule Information](https://wish.wis.ntu.edu.sg/webexe/owa/aus_schedule.main)
- [Exam Timetable](https://wis.ntu.edu.sg/webexe/owa/exam_timetable_und.main)

# Pre-requisites

Ensure you have a `.env` file in the same directory as `settings.py` with the following properties set

```
# Secret key for generating an authentication token
SECRET_KEY=

# Name of the postgres database
DBNAME=ntumods

# Username to access the postgres database
DBUSERNAME=postgres

# Password of the user
DBPASSWORD=password
```

# Starting NTUMods

1. Install python packages
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Build the React app

From root:
```
cd frontend
npm install --legacy-peer-deps
npm run build
```

3. Copy the build to django
```
cp -r build ../backend/
```

4. Setup and run django
```
cd ../backend
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

# To Dos

- Scrape professors
- Login & Timetable
- Mix venue searches together
