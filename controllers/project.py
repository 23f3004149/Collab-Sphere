from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from flask_login import login_required,current_user
from models import db,Project,Comment,Skill
from sqlalchemy.orm import joinedload


project_bp = Blueprint('project',__name__)

@project_bp.route('/project')
def project():

    projects = Project.query.all()
    search_query = request.args.get("search", "").strip().lower()
    difficulty = request.args.get("skill_level", "All")
    technology = request.args.get("technology", "All")
    sort_by = request.args.get("sort", "desc")

    projects_query = Project.query

    if search_query:
        projects_query = projects_query.filter(
            Project.title.ilike(f"%{search_query}%") |
            Project.description.ilike(f"%{search_query}%")
        )

    if difficulty != "All":
        projects_query = projects_query.filter(Project.difficulty == difficulty)

    if technology != "All":
        projects_query = projects_query.join(Project.skills).filter(Skill.name == technology)


    if sort_by == "asc":
        projects_query = projects_query.order_by(Project.created_at.asc())
    else:
        projects_query = projects_query.order_by(Project.created_at.desc())

    
    all_skills = Skill.query.order_by(Skill.name).all()

    projects = projects_query.all()

    return render_template('projects.html', projects=projects,
                            skills=all_skills,
                            search_query=search_query,
                            difficulty=difficulty,
                            technology=technology,
                            sort_by=sort_by)


@project_bp.route('/create-project', methods=['GET', 'POST'])
@login_required
def create_project():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        selected_skill_ids = request.form.getlist('skills')  
        difficulty = request.form['difficulty']
        repo_url = request.form['repo_url']

        selected_skills = Skill.query.filter(Skill.id.in_(selected_skill_ids)).all()

        new_project = Project(
            title=title,
            description=description,
            difficulty=difficulty,
            repo_url=repo_url,
            user_id=current_user.id,
            skills=selected_skills
        )

        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('user.myproject'))

    skills = Skill.query.order_by(Skill.name).all()
    return render_template('create_project.html', skills=skills)

@project_bp.route('/project/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)

    if project.user_id != session['user_id']:
        flash("You are not authorized to delete this project.", "danger")
        return redirect(url_for('project.project_detail', project_id=project_id))

    db.session.delete(project)
    db.session.commit()
    flash("Project deleted successfully.", "success")
    return redirect(url_for('user.myproject')) 


@project_bp.route('/project/<int:project_id>', methods=['GET'])
@login_required
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    comments = Comment.query.filter_by(project_id=project_id).options(joinedload(Comment.author)).all()
    interest_count = len(list(project.interests))
    user_has_interested = any(interest.user_id == current_user.id for interest in project.interests)
    
    return render_template(
        'project_detail.html',
        project=project,
        comments=comments,
        interest_count=interest_count,
        user_has_interested=user_has_interested
    )


