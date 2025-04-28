from flask import Flask, render_template, redirect, url_for, request, session
from models import db, User, Project, Interest, Comment
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change it later
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return "Welcome to collab-Sphere"
    #projects = Project.query.all()
    #return render_template('home.html', projects=projects)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
