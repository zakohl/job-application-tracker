-- Job Application Tracker 
-- Database Schema
-- COP4751 (Advanced Database Management)
 
DROP DATABASE IF EXISTS job_tracker;
CREATE DATABASE job_tracker;
USE job_tracker;
 
-- Table: companies

CREATE TABLE companies (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    industry VARCHAR(50),
    website VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(50),
    notes TEXT
);
 
-- Table: jobs

CREATE TABLE jobs (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    job_title VARCHAR(100) NOT NULL,
    job_type ENUM('Full-time', 'Part-time', 'Contract', 'Internship') DEFAULT 'Full-time',
    salary_min INT,
    salary_max INT,
    job_url VARCHAR(300),
    date_posted DATE,
    requirements JSON,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);
 
-- Table: applications

CREATE TABLE applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    application_date DATE NOT NULL,
    status ENUM('Applied', 'Screening', 'Interview', 'Offer', 'Rejected', 'Withdrawn') DEFAULT 'Applied',
    resume_version VARCHAR(50),
    cover_letter_sent BOOLEAN DEFAULT FALSE,
    interview_data JSON,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE
);
 
-- Table: contacts

CREATE TABLE contacts (
    contact_id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    contact_name VARCHAR(100) NOT NULL,
    title VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    linkedin_url VARCHAR(200),
    notes TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);
 
-- Indexes for performance

CREATE INDEX idx_job_title ON jobs(job_title);
CREATE INDEX idx_job_type ON jobs(job_type);
CREATE INDEX idx_app_status ON applications(status);
CREATE INDEX idx_company_industry ON companies(industry);
 
-- Sample Data

INSERT INTO companies (company_name, industry, website, city, state) VALUES
('Tech Solutions Inc', 'Technology', 'www.techsolutions.com', 'Miami', 'Florida'),
('Data Analytics Corp', 'Data Science', 'www.dataanalytics.com', 'Austin', 'Texas'),
('Cloud Systems LLC', 'Cloud Computing', 'www.cloudsystems.com', 'Seattle', 'Washington'),
('Digital Innovations', 'Software', 'www.digitalinnovations.com', 'San Francisco', 'California'),
('Smart Tech Group', 'AI/ML', 'www.smarttech.com', 'Boston', 'Massachusetts');
 
INSERT INTO jobs (company_id, job_title, salary_min, salary_max, job_type, date_posted, requirements) VALUES
(1, 'Software Developer', 70000, 90000, 'Full-time', '2025-01-15',
 '{"required_skills": ["Python", "SQL", "Git"], "preferred_skills": ["Flask", "Docker", "AWS"], "education": "Bachelor in CS", "experience_years": 2}'),
(1, 'Database Administrator', 75000, 95000, 'Full-time', '2025-01-10',
 '{"required_skills": ["SQL", "MySQL", "Linux"], "preferred_skills": ["PostgreSQL", "MongoDB"], "education": "Bachelor in CS", "experience_years": 3}'),
(2, 'Data Analyst', 65000, 85000, 'Full-time', '2025-01-12',
 '{"required_skills": ["SQL", "Excel", "Tableau"], "preferred_skills": ["Python", "R"], "education": "Bachelor degree", "experience_years": 1}'),
(3, 'Cloud Engineer', 80000, 100000, 'Full-time', '2025-01-08',
 '{"required_skills": ["AWS", "Docker", "Linux"], "preferred_skills": ["Kubernetes", "Terraform"], "education": "Bachelor in CS", "experience_years": 3}'),
(4, 'Junior Developer', 55000, 70000, 'Full-time', '2025-01-14',
 '{"required_skills": ["Python", "HTML", "CSS"], "preferred_skills": ["JavaScript", "Flask"], "education": "Bachelor in CS", "experience_years": 0}'),
(4, 'Senior Developer', 95000, 120000, 'Full-time', '2025-01-14',
 '{"required_skills": ["Python", "SQL", "Flask", "Docker"], "preferred_skills": ["AWS", "React", "CI/CD"], "education": "Bachelor in CS", "experience_years": 5}'),
(5, 'ML Engineer', 90000, 115000, 'Full-time', '2025-01-11',
 '{"required_skills": ["Python", "TensorFlow", "SQL"], "preferred_skills": ["PyTorch", "Docker", "AWS"], "education": "Master in CS or related", "experience_years": 2}');
 
INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent, interview_data) VALUES
(1, '2025-01-16', 'Applied', 'v2.1', TRUE, NULL),
(3, '2025-01-13', 'Interview', 'v2.1', TRUE,
 '{"interview_rounds": 2, "interviewers": ["Sarah Johnson", "Mike Chen"], "feedback": "Strong technical skills"}'),
(4, '2025-01-09', 'Rejected', 'v2.0', FALSE, NULL),
(5, '2025-01-15', 'Applied', 'v2.1', TRUE, NULL),
(7, '2025-01-12', 'Screening', 'v2.1', TRUE,
 '{"interview_rounds": 1, "interviewers": ["Emily Williams"], "feedback": "Promising candidate"}');
 
INSERT INTO contacts (company_id, contact_name, title, email, phone, linkedin_url, notes) VALUES
(1, 'Sarah Johnson', 'HR Manager', 'sjohnson@techsolutions.com', '305-555-0101', 'linkedin.com/in/sjohnson', 'Met at career fair'),
(2, 'Michael Chen', 'Technical Recruiter', 'mchen@dataanalytics.com', '512-555-0202', 'linkedin.com/in/mchen', NULL),
(3, 'Emily Williams', 'Hiring Manager', 'ewilliams@cloudsystems.com', NULL, 'linkedin.com/in/ewilliams', 'Referred by a friend'),
(4, 'David Brown', 'Senior Developer', NULL, '415-555-0404', NULL, NULL),
(5, 'Lisa Garcia', 'Talent Acquisition', 'lgarcia@smarttech.com', '617-555-0505', 'linkedin.com/in/lgarcia', 'Very responsive');