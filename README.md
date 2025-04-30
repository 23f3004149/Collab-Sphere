
# Collab-Sphere

A platform for students to share open-source project ideas and collaborate with others.

## Features

- User Authentication (login, register, logout)
- User Profiles with customizable skills
- Project Creation and Management
- Project Browsing with filters
- Interest Tracking System
- Discussion Section for each project

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd collab-sphere
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

Create a `.env` file in the project root with the following content:

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-goes-here-change-in-production
```

5. Initialize the database and seed initial data:

```bash
python seeds.py
```

6. Run the application:

```bash
python run.py
```

The application will be available at http://localhost:5000

## Test Users

After seeding the database, the following test users are available:

1. Username: testuser
   Email: testuser@gmail.com
   Password: password123

2. Username: demostudent
   Email: demostudent@gmail.com
   Password: student123