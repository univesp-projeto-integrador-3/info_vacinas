# project/server/main/forms.py
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Regexp


class ConsultaCalendarioForm(FlaskForm):
    data_nascimento = DateField(
        "Data de nascimento", [DataRequired()])

    is_gestante = SelectField(u'Você é gestante?', choices=[
        ('0', 'Não'),
        ('1', 'Sim')
    ])


class ConsultaUbsForm(FlaskForm):
    cep = StringField(
        "CEP", [Regexp(
            "[0-9]{5}-[0-9]{3}",
            flags=0,
            message='CEP Inválido. Digite o cep no formato 12345-000.')
        ])
