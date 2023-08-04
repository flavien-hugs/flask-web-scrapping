from flask import abort
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from src.services.account import Project
from src.services.account import utils
from src.services.account.forms import ProjectForm


dashboard_bp = Blueprint("dashboard_bp", __name__, url_prefix="/panel/")


@dashboard_bp.get("/")
@login_required
def dashboard():
    page_title = "Tableau de bord"
    return render_template(
        "dashboard/index.html", page_title=page_title, user=current_user
    )


@dashboard_bp.get("/results/<string:public_id>")
@login_required
def read_project(public_id):
    project = utils.abort_if_project_doesnt_exist(public_id)
    page_title = project.name
    return render_template(
        "project/read.html", user=current_user, page_title=page_title, project=project
    )


@dashboard_bp.route("/update/<string:public_id>", methods=["GET", "POST"])
@login_required
def update_project(public_id):
    page_title = "Mettre à jour les mots-clés/phrases-clés"
    project = utils.abort_if_project_doesnt_exist(public_id)

    form = ProjectForm()
    if form.validate_on_submit():
        keywords = form.name.data.split(",")
        name_data = keywords[0].strip()
        Project.update(project, name_data)
        return redirect(url_for("dashboard_bp.dashboard"))
    return render_template(
        "project/update.html", form=form, page_title=page_title, project=project
    )


@dashboard_bp.post("/delete/<string:public_id>/")
@login_required
def delete_project(public_id):
    project = utils.abort_if_project_doesnt_exist(public_id)
    if project.user_id != current_user.id:
        abort(403)
    project.delete()
    return redirect(url_for("dashboard_bp.dashboard"))
