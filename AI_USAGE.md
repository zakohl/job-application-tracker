# AI Usage Documentation

## Tools Used

- **Claude** (Anthropic) – Used throughout the development as a learning resource for understanding Flask, debugging issues, and verifying my implementation against the project requirements.

## Key Prompts and How They Helped

### Getting Started with Flask
- "I've never used Flask before. How does a basic Flask app work and what files do I need to set up a project with templates and a database connection?"
- "What is a Jinja2 template and how does it connect to my Flask routes?"
- "How do I structure a Flask project that has multiple pages for different database tables?"

These prompts helped me understand the Flask project structure before writing any code. I learned about routes, `render_template`, and how the `templates/` folder works.

### Connecting Flask to My Existing MySQL Database
- "I already have a MySQL database called job_tracker from my coursework. How do I connect to it from Flask using mysql-connector-python?"
- "In Assignment 5 we built a JobTrackerDB class. How would I adapt that pattern for use in a Flask web app?"
- "What is the difference between using a class-based approach vs standalone functions for database helpers in Flask?"

I had the Python database connection knowledge from Assignment 5 but I needed help adapting it to work within Flask's request cycle.

### Building CRUD Operations
- "How do I create a Flask route that handles both displaying a form (GET) and processing the submission (POST)?"
- "What is the correct way to get form data from an HTML form in Flask?"
- "How do I pass data from my Python route to an HTML template so I can pre-fill an edit form?"
- "How should I handle the delete operation safely — should it be a GET or POST request?"

I built the companies CRUD first and then used that as a pattern for the other three tables.

### Working with JSON and the Job Match Feature
- "I have a JSON column called requirements in my jobs table from Assignment 7. How do I parse that JSON in Python to compare skills?"
- "What is a good algorithm for calculating a match percentage between a user's skills and a job's required skills?"
- "How do I display the match results in HTML with a progress bar showing the percentage?"

### Debugging and Verification
- "I'm getting a 'MySQL connector not finding database' error when I run my Flask app. What should I check?"
- "Can you review my project against this rubric and tell me if I'm missing any required features?"
- "My foreign key delete is failing — how does ON DELETE CASCADE work and should I add it to my schema?"

## What Worked Well

- Asking Flask questions in the context of what I already knew from Assignment 5 made the learning curve more manageable
- Building one table's CRUD first (companies) and then asking how to replicate the pattern for the remaining tables saved a lot of time
- Using AI to explain error messages was faster than searching through Stack Overflow
- Asking AI to check my project against the rubric caught a couple things I missed, like the JSON columns and the AI_USAGE.md file itself

## What I Modified from AI Suggestions

- AI initially suggested a class-based database module but I went with standalone functions since they were simpler for this project's scope
- Changed column names to match the exact project specification schema (e.g., `contact_name` instead of separate `first_name`/`last_name`)
- Added confirmation dialogs on delete buttons — AI's initial examples didn't include these
- Customized the status badges and color scheme in CSS to my own preference
- Added input validation and edge case handling that AI's initial examples skipped
- Adjusted the job match algorithm to be case-insensitive after testing revealed it was missing matches

## Lessons Learned

- Flask is essentially just a way to run the same SQL operations I was doing in Workbench, but triggered by web requests instead of the lightning bolt button
- The `database.py` module is very similar to what we built in Assignment 5 — the main difference is returning the data to templates instead of printing to the console
- AI is great for learning a new framework quickly, but I still needed to understand my own database schema to make things work correctly
- Testing each route manually after building it caught issues that weren't accounted for
- Starting with one table and getting full CRUD working before moving to the next was much better than trying to build everything all at once
