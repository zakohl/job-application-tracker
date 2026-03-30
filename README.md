# Job Application Tracker

A full-stack web application to manage and track job applications during the job search process. Built with MySQL, Python/Flask, and HTML/CSS.

**COP4751 – Advanced Database Management – Course Project**

## Features

- **Dashboard** – At-a-glance statistics: total companies, jobs, applications, contacts, status breakdown, and recent activity.
- **Companies** – Full CRUD: add, view, edit, and delete companies you're targeting.
- **Jobs** – Full CRUD with salary ranges, job types, and JSON-stored required skills.
- **Applications** – Track every application with status, resume version, and cover-letter flag.
- **Contacts** – Keep recruiter and hiring-manager details linked to companies.
- **Job Match** – Enter your skills and instantly see jobs ranked by match percentage against their required-skills JSON.

## Technologies

| Layer | Technology |
|-------|-----------|
| Database | MySQL 8+ |
| Backend | Python 3 / Flask |
| Frontend | HTML, CSS, Bootstrap 5 |
| Version Control | Git / GitHub |

## Setup Instructions

### 1. Prerequisites

- Python 3.10+ installed (`python --version`)
- MySQL 8.0+ server running locally
- Git (optional, for cloning)

### 2. Clone the Repository

```bash
git clone https://github.com/zakohl/job-application-tracker.git
cd job-application-tracker
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the Database

Open MySQL Workbench (or a terminal) and run the schema script:

```bash
mysql -u root -p < schema.sql
```

Or paste the contents of `schema.sql` into MySQL Workbench and execute.

### 5. Configure Your Password

Open `database.py` and replace `YOUR_PASSWORD_HERE` with your MySQL root password:

```python
'password': 'YOUR_PASSWORD_HERE',
```

### 6. Run the Application

```bash
python app.py
```

Open your browser and go to **http://127.0.0.1:5000**

## Project Structure

```
job_tracker/
├── app.py              # Main Flask application (routes)
├── database.py         # Database connection & helper functions
├── schema.sql          # SQL script to create the database & seed data
├── requirements.txt    # Python dependencies
├── AI_USAGE.md         # GenAI usage documentation
├── README.md           # This file
├── templates/          # Jinja2 HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── companies.html
│   ├── jobs.html
│   ├── applications.html
│   ├── contacts.html
│   └── job_match.html
└── static/
    └── style.css       # Custom stylesheet
```

## Database Schema

Four tables with proper foreign keys and JSON columns:

- **companies** – company_id (PK), company_name, industry, website, city, state, notes
- **jobs** – job_id (PK), company_id (FK), job_title, job_type (ENUM), salary_min/max, requirements (JSON)
- **applications** – application_id (PK), job_id (FK), application_date, status (ENUM), interview_data (JSON)
- **contacts** – contact_id (PK), company_id (FK), contact_name, title, email, phone, linkedin_url, notes

## License

This project was created for academic purposes as part of COP4751 at FIU.
