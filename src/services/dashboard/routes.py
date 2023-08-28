from itertools import chain

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

from .func_utils import(
    Facebook,
    Instagram,
    CombinedData
)


dashboard_bp = Blueprint("dashboard_bp", __name__, url_prefix="/panel/~/")


@dashboard_bp.get("/dashboard/")
@login_required
def dashboard():
    page_title = "Tableau de bord"
    data = CombinedData(current_user)
    items_data = data.get_combined_data()
    stats_data = data.get_statistics()

    stat_fb = data.get_stat_facebook()
    stat_insta = data.get_stat_instagram()

    return render_template(
        "dashboard/_base.html",
        page_title=page_title,
        user=current_user,
        items=items_data,
        stat=stats_data,
        stat_fb=stat_fb,
        stat_insta=stat_insta
    )


@dashboard_bp.get("/project/")
@login_required
def get_projects():
    page_title = "projets"
    projects = Project.all(current_user)
    return render_template(
        "project/list.html",
        user=current_user,
        page_title=page_title.capitalize(),
        projects=projects
    )


@dashboard_bp.get("/result/<string:public_id>")
@login_required
def detail_project(public_id: str):
    project = utils.abort_if_project_doesnt_exist(public_id)

    page_title = project.name
    page_title = f"Tag '{project.name}' data"

    data = CombinedData(current_user)
    items_data = data.get_detail(project.name)
    stats_data = data.get_statistics()

    stat_fb = data.get_stat_facebook()
    stat_insta = data.get_stat_instagram()


    return render_template(
        "project/detail.html",
        project=project,
        user=current_user,
        page_title=page_title,
        item=items_data,
        stat=stats_data,
        stat_fb=stat_fb,
        stat_insta=stat_insta
    )


@dashboard_bp.get("/result/~/fb/<string:public_id>")
@login_required
def facebook_detail_project(public_id: str):
    project = utils.abort_if_project_doesnt_exist(public_id)

    page_title = f"Facebook data : '{project.name}'"

    data = Facebook(current_user)
    items_data = data.get_detail(project.name)
    stats_data = data.get_statistic(project.name)

    return render_template(
        "project/fb.html",
        project=project,
        user=current_user,
        page_title=page_title,
        item=items_data,
        stat=stats_data
    )


@dashboard_bp.get("/result/~/in/<string:public_id>")
@login_required
def instagram_detail_project(public_id: str):
    project = utils.abort_if_project_doesnt_exist(public_id)

    page_title = f"Instagram data : '{project.name}'"

    data = Instagram(current_user)
    items_data = data.get_detail(project.name)
    stats_data = data.get_statistic(project.name)

    return render_template(
        "project/fb.html",
        project=project,
        user=current_user,
        page_title=page_title,
        item=items_data,
        stat=stats_data
    )



@dashboard_bp.route("/update/<string:public_id>", methods=["GET", "POST"])
@login_required
def update_project(public_id: str):
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
def delete_project(public_id: str):
    project = utils.abort_if_project_doesnt_exist(public_id)
    if project.user_id != current_user.id:
        abort(403)
    project.delete()
    return redirect(url_for("dashboard_bp.dashboard"))
