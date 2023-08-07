from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from src.services.account import Project
from src.services.account.forms import ProjectForm


project_bp = Blueprint("project_bp", __name__, url_prefix="/projects/")


@project_bp.route("/add/", methods=["GET", "POST"])
@login_required
def create_project():
    page_title = "Saisir des mots-clés/phrases-clés"

    form = ProjectForm()
    if form.validate_on_submit():
        keywords = form.name.data.split(",")
        for key in keywords:
            project = Project(name=key.strip(), user=current_user._get_current_object())
            project.save()
        return redirect(url_for("dashboard_bp.dashboard"))
    return render_template("project/create.html", form=form, page_title=page_title)
