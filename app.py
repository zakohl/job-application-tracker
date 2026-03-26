from flask import Flask, render_template, request, redirect, url_for, flash
import database as db
import json

app = Flask(__name__)
app.secret_key = 'job-tracker-secret-key-change-in-production'


# Dashboard
@app.route('/')
def dashboard():
    stats = db.get_dashboard_stats()
    return render_template('dashboard.html', stats=stats)


# Companies  (CRUD)
@app.route('/companies')
def companies():
    rows = db.get_all_companies()
    return render_template('companies.html', companies=rows)


@app.route('/companies/add', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        db.add_company(request.form)
        flash('Company added successfully!', 'success')
        return redirect(url_for('companies'))
    rows = db.get_all_companies()
    return render_template('companies.html', companies=rows, show_form=True, company=None)


@app.route('/companies/edit/<int:company_id>', methods=['GET', 'POST'])
def edit_company(company_id):
    if request.method == 'POST':
        db.update_company(company_id, request.form)
        flash('Company updated successfully!', 'success')
        return redirect(url_for('companies'))
    rows = db.get_all_companies()
    company = db.get_company(company_id)
    return render_template('companies.html', companies=rows, show_form=True, company=company)


@app.route('/companies/delete/<int:company_id>', methods=['POST'])
def delete_company(company_id):
    db.delete_company(company_id)
    flash('Company deleted.', 'info')
    return redirect(url_for('companies'))


# Jobs  (CRUD)
@app.route('/jobs')
def jobs():
    rows = db.get_all_jobs()
    return render_template('jobs.html', jobs=rows)


@app.route('/jobs/add', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        db.add_job(request.form)
        flash('Job added successfully!', 'success')
        return redirect(url_for('jobs'))
    rows = db.get_all_jobs()
    all_companies = db.get_all_companies()
    return render_template('jobs.html', jobs=rows, show_form=True, job=None, companies=all_companies)


@app.route('/jobs/edit/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    if request.method == 'POST':
        db.update_job(job_id, request.form)
        flash('Job updated successfully!', 'success')
        return redirect(url_for('jobs'))
    rows = db.get_all_jobs()
    job = db.get_job(job_id)
    all_companies = db.get_all_companies()
    skills_str = ''
    if job and job.get('requirements'):
        try:
            req = json.loads(job['requirements']) if isinstance(job['requirements'], str) else job['requirements']
            skills_str = ', '.join(req.get('required_skills', []))
        except (json.JSONDecodeError, TypeError):
            pass
    return render_template('jobs.html', jobs=rows, show_form=True, job=job, companies=all_companies, skills_str=skills_str)


@app.route('/jobs/delete/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    db.delete_job(job_id)
    flash('Job deleted.', 'info')
    return redirect(url_for('jobs'))


# Applications  (CRUD)
@app.route('/applications')
def applications():
    rows = db.get_all_applications()
    return render_template('applications.html', applications=rows)


@app.route('/applications/add', methods=['GET', 'POST'])
def add_application():
    if request.method == 'POST':
        db.add_application(request.form)
        flash('Application added successfully!', 'success')
        return redirect(url_for('applications'))
    rows = db.get_all_applications()
    all_jobs = db.get_all_jobs()
    return render_template('applications.html', applications=rows, show_form=True, application=None, jobs=all_jobs)


@app.route('/applications/edit/<int:application_id>', methods=['GET', 'POST'])
def edit_application(application_id):
    if request.method == 'POST':
        db.update_application(application_id, request.form)
        flash('Application updated successfully!', 'success')
        return redirect(url_for('applications'))
    rows = db.get_all_applications()
    application = db.get_application(application_id)
    all_jobs = db.get_all_jobs()
    return render_template('applications.html', applications=rows, show_form=True, application=application, jobs=all_jobs)


@app.route('/applications/delete/<int:application_id>', methods=['POST'])
def delete_application(application_id):
    db.delete_application(application_id)
    flash('Application deleted.', 'info')
    return redirect(url_for('applications'))


# Contacts  (CRUD)
@app.route('/contacts')
def contacts():
    rows = db.get_all_contacts()
    return render_template('contacts.html', contacts=rows)


@app.route('/contacts/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        db.add_contact(request.form)
        flash('Contact added successfully!', 'success')
        return redirect(url_for('contacts'))
    rows = db.get_all_contacts()
    all_companies = db.get_all_companies()
    return render_template('contacts.html', contacts=rows, show_form=True, contact=None, companies=all_companies)


@app.route('/contacts/edit/<int:contact_id>', methods=['GET', 'POST'])
def edit_contact(contact_id):
    if request.method == 'POST':
        db.update_contact(contact_id, request.form)
        flash('Contact updated successfully!', 'success')
        return redirect(url_for('contacts'))
    rows = db.get_all_contacts()
    contact = db.get_contact(contact_id)
    all_companies = db.get_all_companies()
    return render_template('contacts.html', contacts=rows, show_form=True, contact=contact, companies=all_companies)


@app.route('/contacts/delete/<int:contact_id>', methods=['POST'])
def delete_contact(contact_id):
    db.delete_contact(contact_id)
    flash('Contact deleted.', 'info')
    return redirect(url_for('contacts'))


# Job Match
@app.route('/job-match', methods=['GET', 'POST'])
def job_match():
    results = None
    skills_input = ''
    if request.method == 'POST':
        skills_input = request.form.get('skills', '')
        user_skills = [s.strip() for s in skills_input.split(',') if s.strip()]
        results = db.get_job_matches(user_skills)
    return render_template('job_match.html', results=results, skills_input=skills_input)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
