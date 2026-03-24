import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD_HERE',   # <-- Replace with your MySQL root password
    'database': 'job_tracker'
}


def get_db():
    """Return a new MySQL connection using the project config."""
    return mysql.connector.connect(**DB_CONFIG)


# Companies

def get_all_companies():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM companies ORDER BY company_name')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_company(company_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM companies WHERE company_id = %s', (company_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def add_company(data):
    conn = get_db()
    cursor = conn.cursor()
    query = '''INSERT INTO companies (company_name, industry, website, city, state, notes)
               VALUES (%s, %s, %s, %s, %s, %s)'''
    cursor.execute(query, (
        data['company_name'], data.get('industry', ''),
        data.get('website', ''), data.get('city', ''),
        data.get('state', ''), data.get('notes', '')
    ))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


def update_company(company_id, data):
    conn = get_db()
    cursor = conn.cursor()
    query = '''UPDATE companies
               SET company_name=%s, industry=%s, website=%s, city=%s, state=%s, notes=%s
               WHERE company_id=%s'''
    cursor.execute(query, (
        data['company_name'], data.get('industry', ''),
        data.get('website', ''), data.get('city', ''),
        data.get('state', ''), data.get('notes', ''),
        company_id
    ))
    conn.commit()
    cursor.close()
    conn.close()


def delete_company(company_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM companies WHERE company_id = %s', (company_id,))
    conn.commit()
    cursor.close()
    conn.close()


# Jobs

def get_all_jobs():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT j.*, c.company_name
        FROM jobs j
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY j.date_posted DESC
    ''')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_job(job_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT j.*, c.company_name
        FROM jobs j
        JOIN companies c ON j.company_id = c.company_id
        WHERE j.job_id = %s
    ''', (job_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def add_job(data):
    conn = get_db()
    cursor = conn.cursor()
    import json
    req_json = None
    skills = data.get('required_skills', '')
    if skills:
        skill_list = [s.strip() for s in skills.split(',') if s.strip()]
        req_json = json.dumps({"required_skills": skill_list})

    query = '''INSERT INTO jobs
               (company_id, job_title, job_type, salary_min, salary_max,
                job_url, date_posted, requirements)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
    cursor.execute(query, (
        data['company_id'], data['job_title'], data.get('job_type', 'Full-time'),
        data.get('salary_min') or None, data.get('salary_max') or None,
        data.get('job_url', ''), data.get('date_posted') or None,
        req_json
    ))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


def update_job(job_id, data):
    conn = get_db()
    cursor = conn.cursor()
    import json
    req_json = None
    skills = data.get('required_skills', '')
    if skills:
        skill_list = [s.strip() for s in skills.split(',') if s.strip()]
        req_json = json.dumps({"required_skills": skill_list})

    query = '''UPDATE jobs
               SET company_id=%s, job_title=%s, job_type=%s,
                   salary_min=%s, salary_max=%s, job_url=%s,
                   date_posted=%s, requirements=%s
               WHERE job_id=%s'''
    cursor.execute(query, (
        data['company_id'], data['job_title'], data.get('job_type', 'Full-time'),
        data.get('salary_min') or None, data.get('salary_max') or None,
        data.get('job_url', ''), data.get('date_posted') or None,
        req_json, job_id
    ))
    conn.commit()
    cursor.close()
    conn.close()


def delete_job(job_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM jobs WHERE job_id = %s', (job_id,))
    conn.commit()
    cursor.close()
    conn.close()


# Applications

def get_all_applications():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT a.*, j.job_title, c.company_name
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY a.application_date DESC
    ''')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_application(application_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT a.*, j.job_title, c.company_name
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        WHERE a.application_id = %s
    ''', (application_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def add_application(data):
    conn = get_db()
    cursor = conn.cursor()
    query = '''INSERT INTO applications
               (job_id, application_date, status, resume_version, cover_letter_sent)
               VALUES (%s, %s, %s, %s, %s)'''
    cursor.execute(query, (
        data['job_id'], data['application_date'],
        data.get('status', 'Applied'), data.get('resume_version', ''),
        1 if data.get('cover_letter_sent') else 0
    ))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


def update_application(application_id, data):
    conn = get_db()
    cursor = conn.cursor()
    query = '''UPDATE applications
               SET job_id=%s, application_date=%s, status=%s,
                   resume_version=%s, cover_letter_sent=%s
               WHERE application_id=%s'''
    cursor.execute(query, (
        data['job_id'], data['application_date'],
        data.get('status', 'Applied'), data.get('resume_version', ''),
        1 if data.get('cover_letter_sent') else 0,
        application_id
    ))
    conn.commit()
    cursor.close()
    conn.close()


def delete_application(application_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM applications WHERE application_id = %s', (application_id,))
    conn.commit()
    cursor.close()
    conn.close()


# Contacts

def get_all_contacts():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT ct.*, c.company_name
        FROM contacts ct
        JOIN companies c ON ct.company_id = c.company_id
        ORDER BY ct.contact_name
    ''')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_contact(contact_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT ct.*, c.company_name
        FROM contacts ct
        JOIN companies c ON ct.company_id = c.company_id
        WHERE ct.contact_id = %s
    ''', (contact_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def add_contact(data):
    conn = get_db()
    cursor = conn.cursor()
    query = '''INSERT INTO contacts
               (company_id, contact_name, title, email, phone, linkedin_url, notes)
               VALUES (%s, %s, %s, %s, %s, %s, %s)'''
    cursor.execute(query, (
        data['company_id'], data['contact_name'],
        data.get('title', ''), data.get('email', ''),
        data.get('phone', ''), data.get('linkedin_url', ''),
        data.get('notes', '')
    ))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


def update_contact(contact_id, data):
    conn = get_db()
    cursor = conn.cursor()
    query = '''UPDATE contacts
               SET company_id=%s, contact_name=%s, title=%s,
                   email=%s, phone=%s, linkedin_url=%s, notes=%s
               WHERE contact_id=%s'''
    cursor.execute(query, (
        data['company_id'], data['contact_name'],
        data.get('title', ''), data.get('email', ''),
        data.get('phone', ''), data.get('linkedin_url', ''),
        data.get('notes', ''), contact_id
    ))
    conn.commit()
    cursor.close()
    conn.close()


def delete_contact(contact_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE contact_id = %s', (contact_id,))
    conn.commit()
    cursor.close()
    conn.close()


# Dashboard statistics

def get_dashboard_stats():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    stats = {}

    cursor.execute('SELECT COUNT(*) AS count FROM companies')
    stats['companies'] = cursor.fetchone()['count']

    cursor.execute('SELECT COUNT(*) AS count FROM jobs')
    stats['jobs'] = cursor.fetchone()['count']

    cursor.execute('SELECT COUNT(*) AS count FROM applications')
    stats['applications'] = cursor.fetchone()['count']

    cursor.execute('SELECT COUNT(*) AS count FROM contacts')
    stats['contacts'] = cursor.fetchone()['count']

    cursor.execute('''
        SELECT status, COUNT(*) AS count
        FROM applications
        GROUP BY status ORDER BY count DESC
    ''')
    stats['by_status'] = cursor.fetchall()

    cursor.execute('''
        SELECT a.application_id, a.application_date, a.status,
               j.job_title, c.company_name
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY a.application_date DESC LIMIT 5
    ''')
    stats['recent'] = cursor.fetchall()

    cursor.execute('''
        SELECT ROUND(AVG(salary_min)) AS avg_min, ROUND(AVG(salary_max)) AS avg_max
        FROM jobs WHERE salary_min IS NOT NULL
    ''')
    sal = cursor.fetchone()
    stats['avg_salary_min'] = sal['avg_min'] or 0
    stats['avg_salary_max'] = sal['avg_max'] or 0

    cursor.close()
    conn.close()
    return stats


# Job Match

def get_job_matches(user_skills):
    """
    Compare user skills against each job's required_skills JSON field.
    Returns a list of jobs ranked by match percentage.
    """
    import json
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT j.job_id, j.job_title, j.salary_min, j.salary_max,
               j.requirements, c.company_name
        FROM jobs j
        JOIN companies c ON j.company_id = c.company_id
        WHERE j.requirements IS NOT NULL
    ''')
    jobs = cursor.fetchall()
    cursor.close()
    conn.close()

    user_skills_lower = [s.strip().lower() for s in user_skills if s.strip()]
    results = []

    for job in jobs:
        try:
            req = json.loads(job['requirements']) if isinstance(job['requirements'], str) else job['requirements']
            required = [s.lower() for s in req.get('required_skills', [])]
        except (json.JSONDecodeError, TypeError):
            continue

        if not required:
            continue

        matched = [s for s in required if s in user_skills_lower]
        missing = [s for s in required if s not in user_skills_lower]
        pct = round(len(matched) / len(required) * 100)

        results.append({
            'job_id': job['job_id'],
            'job_title': job['job_title'],
            'company_name': job['company_name'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max'],
            'match_pct': pct,
            'matched_skills': matched,
            'missing_skills': missing,
            'total_required': len(required)
        })

    results.sort(key=lambda x: x['match_pct'], reverse=True)
    return results
