from flask import Blueprint
from flask import render_template, url_for, redirect

from flask_login import current_user
from flask_login import login_required

from src.services.account import Project
from src.services.account.forms import ProjectForm


project_bp = Blueprint("project_bp", __name__, url_prefix="/projects/")



@project_bp.route("/create/", methods=["GET", "POST"])
@login_required
def create_project():
    page_title = "Créer votre projet"

    form = ProjectForm()
    if form.validate_on_submit():
        create_project = Project(
            name=form.name.data.lower(),
            user=current_user._get_current_object()
        )
        create_project.save()
        return redirect(url_for("dashboard_bp.dashboard"))
    return render_template("project/create.html", form=form, page_title=page_title)
