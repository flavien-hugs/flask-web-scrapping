from flask import Blueprint
from flask import render_template
from flask_login import current_user
from flask_login import login_required


dashboard_bp = Blueprint("dashboard_bp", __name__, url_prefix="/account/")


@dashboard_bp.get("/dashboard/")
@login_required
def dashboard():
    page_title = "Tableau de bord"
    return render_template(
        "dashboard/index.html",
        page_title=page_title,
        current_user=current_user
    )
