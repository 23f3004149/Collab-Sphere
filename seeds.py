from app import app, db
from models import User, Skill, Project
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt(app)

def seed_database():
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        if User.query.count() > 0:
            print("Database already contains data. Skipping seeding.")
            return

        print("Adding skills...")
        skills = [
            'Python', 'JavaScript', 'HTML/CSS', 'React', 'Vue.js', 'Angular',
            'Node.js', 'Flask', 'Django', 'Express', 'MongoDB', 'PostgreSQL',
            'MySQL', 'SQLite', 'Docker', 'Kubernetes', 'AWS', 'Azure',
            'Git', 'RESTful API', 'GraphQL', 'TensorFlow', 'PyTorch', 'Machine Learning',
            'Data Science', 'Natural Language Processing', 'Computer Vision'
        ]

        for skill_name in skills:
            skill = Skill(name=skill_name)
            db.session.add(skill)

        db.session.commit()

        print("Creating test users...")
        users = [
            {
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123',
                'bio': 'I am a test user who loves open source!',
                'skills': ['Python', 'JavaScript', 'Flask', 'React']
            },
            {
                'username': 'demostudent',
                'email': 'demo@student.edu',
                'password': 'student123',
                'bio': 'Computer Science student looking for projects to contribute to.',
                'skills': ['Python', 'JavaScript', 'HTML/CSS', 'Git']
            }
        ]

        created_users = []
        for user_data in users:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                bio=user_data['bio'],
                password_hash=bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
            )
            for skill_name in user_data['skills']:
                skill = Skill.query.filter_by(name=skill_name).first()
                if skill:
                    user.skills.append(skill)
            db.session.add(user)
            created_users.append(user)

        db.session.commit()

        print("Creating sample projects...")
        projects = [
            {
                'creator': 'testuser',
                'title': 'Open Source Task Manager',
                'description': 'A task manager app built with Flask and React.',
                'github_link': 'https://github.com/example/task-manager',
                'difficulty': 'Beginner',
                'skills': ['Python', 'JavaScript', 'Flask', 'React']
            },
            {
                'creator': 'testuser',
                'title': 'Machine Learning Image Classifier',
                'description': 'Image classification using TensorFlow.',
                'github_link': 'https://github.com/example/image-classifier',
                'difficulty': 'Advanced',
                'skills': ['Python', 'TensorFlow', 'Machine Learning', 'Computer Vision']
            },
            {
                'creator': 'demostudent',
                'title': 'Study Group Finder App',
                'description': 'App to help students find study groups.',
                'github_link': 'https://github.com/example/study-group-finder',
                'difficulty': 'Intermediate',
                'skills': ['JavaScript', 'Node.js', 'MongoDB', 'HTML/CSS']
            }
        ]

        for project_data in projects:
            creator = User.query.filter_by(username=project_data['creator']).first()
            if creator:
                project = Project(
                    title=project_data['title'],
                    description=project_data['description'],
                    repo_url=project_data['github_link'],
                    difficulty=project_data['difficulty'],
                    author=creator
                )
                for skill_name in project_data['skills']:
                    skill = Skill.query.filter_by(name=skill_name).first()
                    if skill:
                        project.skills.append(skill)
                db.session.add(project)

        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()

