from flask import(
    Blueprint, render_template,
    flash, redirect, url_for, request
)
from flask_login import login_user, current_user

from src.services.account import User
from src.services.account.forms import LoginForm, SignupForm


auth_bp = Blueprint("auth_bp", __name__, url_prefix="/user/")


@auth_bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()


@auth_bp.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("account_bp.dashboard"))

    form = LoginForm(request.form)
    if form.validate_on_submit():
        addr_email = form.addr_email.data
        user = User.find_by_email(addr_email)
        if user and user.is_active and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            next_page = request.args.get("next")
            if next_page is None or not next_page.startswith("/"):
                next_page = url_for("dashboard_bp.dashboard")
            return redirect(next_page)
        else:
            if not user.is_active:
                error_message = "L'utilisateur n'existe pas ou le compte a\
                    été désactivé ! Veuillez contacter l'administrateur système."
            if not user.check_password(form.password.data):
                error_message = "Le mot de passe invalide."

            flash(error_message, category="danger")

    page_title = "Se connecter"
    return render_template("account/login.html", page_title=page_title, form=form)


@auth_bp.route("/register-account/", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated and current_user.is_active:
        flash("Vous êtes déjà inscrit(e).", category="info")
        return redirect(url_for("dashboard_bp.dashboard"))

    form = SignupForm()
    if form.validate_on_submit():
        user_to_create = User(addr_email=form.addr_email.data.lower())
        user_to_create.set_password(form.password.data)
        user_to_create.save()
        msg_success = f"""
            Hey {user_to_create.addr_email},
            votre compte a été créé ! Connectez-vous maintenant !
        """
        flash(msg_success, category="success")
        login_user(user_to_create)
        return redirect(url_for("project_bp.create_project"))

    page_title = "Créer votre compte"
    return render_template("account/signup.html", form=form, page_title=page_title)
