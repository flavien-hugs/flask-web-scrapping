from flask_wtf import FlaskForm
from src.services.account import User
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import InputRequired
from wtforms.validators import Length
from wtforms.validators import ValidationError


class LoginForm(FlaskForm):
    addr_email = StringField(
        "Adresse e-mail",
        render_kw={"required": True},
        validators=[
            DataRequired(),
            InputRequired(),
            Email(message="Entrer une adresse email valide."),
        ],
    )
    password = PasswordField(
        "Mot de passe",
        render_kw={"required": True},
        validators=[InputRequired(), DataRequired()],
    )
    remember_me = BooleanField("Se souvenir de moi")
    submit = SubmitField("Se connecter")


class SignupForm(FlaskForm):
    addr_email = StringField(
        "Adresse email",
        validators=[
            DataRequired(),
            InputRequired(),
            Email(message="Entrer une adresse email valide."),
        ],
        render_kw={"required": True},
    )
    password = PasswordField(
        "Mot de passe",
        render_kw={"required": True},
        validators=[
            DataRequired(),
            Length(min=6, max=20, message="Choisissez un mot de passe plus fort."),
        ],
    )
    confirm_password = PasswordField(
        "Confirmer le mot de passe",
        render_kw={"required": True},
        validators=[
            DataRequired(),
            EqualTo("password", message="Les deux mots de passe ne correspondent pas."),
        ],
    )
    submit = SubmitField("Créer votre compte")

    def validate_addr_email(self, field):
        user = User.find_by_email(field.data.lower())
        if user:
            raise ValidationError(
                f"""
                Cet email '{field.data.lower()}!r' est déjà utilisé.
                Veuillez choisir un autre nom !
                """
            )


class PasswordResetForm(FlaskForm):
    new_password = PasswordField(
        "Nouveau mot de passe",
        render_kw={"required": True},
        validators=[DataRequired()],
    )
    confirm_password = PasswordField(
        "Confirmer le mot de passe",
        render_kw={"required": True},
        validators=[
            DataRequired(),
            EqualTo(
                "confirm_password",
                message="Les deux mots de passe ne correspondent pas.",
            ),
        ],
    )


class ChangePasswordForm(PasswordResetForm):
    old_password = PasswordField(
        "Ancien mot de passe", render_kw={"required": True}, validators=[DataRequired()]
    )


class PasswordResetRequestForm(FlaskForm):
    addr_email = StringField(
        "Votre adresse e-mail",
        render_kw={"required": True},
        validators=[
            DataRequired(),
            Length(1, 64),
            InputRequired(),
            Email(message="Entrer une adresse email valide."),
        ],
    )
    submit = SubmitField("envoyer le lien de réinitialisation")


class ProjectForm(FlaskForm):
    name = StringField(
        "Entrez la marque, le concurrent ou le hashtag à surveiller",
        render_kw={"required": True},
        validators=[DataRequired(), InputRequired()],
    )
    submit = SubmitField("Créer le projet")
