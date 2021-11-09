# project/server/main/forms.py
from flask_wtf import FlaskForm
from wtforms import DateField, PasswordField, SelectField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class ConsultaCalendarioForm(FlaskForm):
    nome = StringField(u'Nome', [DataRequired(), Length(min=3, max=100)])
    data_nascimento = DateField(
        "Data de nascimento", [DataRequired()], format="%d/%m/%Y")
    is_gestante = SelectField(u'Você está gestante?', choices=[(
        None, 'Você está gestante?'), (True, 'Sim'), (False, 'Não')])
