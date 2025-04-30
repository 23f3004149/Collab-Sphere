from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from flask_login import login_user, logout_user, login_required
from models import db, User,Project,Interest,Comment,Skill

user_bp = Blueprint('user',__name__)

@user_bp.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    interested_projects = Interest.query.filter_by(user_id=user.id).all()
    
    return render_template('profile.html', user=user, interested_projects=interested_projects)

@user_bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        user.username = request.form.get('username')
        user.bio = request.form.get('bio')

        # Commit changes to the database
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('user.profile'))

    return render_template('edit_profile.html', user=user)

@user_bp.route('/myproject')
@login_required
def myproject():
    user = User.query.get(session['user_id'])
    created_projects = Project.query.filter_by(user_id=user.id).all()
    return render_template('myprojects.html', user=user, created_projects=created_projects)


@user_bp.route('/edit-skills', methods=['GET', 'POST'])
@login_required
def edit_skills():
    user = User.query.get(session['user_id'])
    all_skills = Skill.query.all()  # Get all available skills for the form

    if request.method == 'POST':
        selected_skill_ids = request.form.getlist('skills')  # Get selected skill IDs as list
        selected_skills = Skill.query.filter(Skill.id.in_(selected_skill_ids)).all()
        user.skills = selected_skills  # Update user's skills
        db.session.commit()
        return redirect(url_for('user.profile'))

    return render_template('edit_skills.html', user=user, all_skills=all_skills)


@user_bp.route('/project/<int:project_id>/comment', methods=['POST'])
@login_required
def add_comment(project_id):

    content = request.form['content']
    new_comment = Comment(content=content, user_id=session['user_id'], project_id=project_id)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('project.project_detail', project_id=project_id))

@user_bp.route('/project/<int:project_id>/interested', methods=['POST'])
@login_required
def express_interest(project_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login')) 

    existing_interest = Interest.query.filter_by(user_id=user_id, project_id=project_id).first()
    if not existing_interest:
        new_interest = Interest(user_id=user_id, project_id=project_id)
        db.session.add(new_interest)
        db.session.commit()

    return redirect(url_for('project.project_detail', project_id=project_id))
