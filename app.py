from flask import Flask, render_template
from models import db, User, Project
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from datetime import timedelta

app = Flask(__name__)

app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///collab_sphere.db'

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


from controllers.auth import auth_bp
from controllers.project import project_bp
from controllers.user import user_bp

app.register_blueprint(project_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
