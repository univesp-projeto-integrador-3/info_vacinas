# project/server/main/views.py
from datetime import datetime

from dateutil.relativedelta import relativedelta
from flask import (Blueprint, Markup, flash, redirect, render_template,
                   request, url_for)
from project.server.main.forms import ConsultaCalendarioForm

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def home():
    return redirect(url_for("main.consulta_calendario"))


@main_blueprint.route("/sobre")
def sobre():
    return render_template("main/sobre.html")


@main_blueprint.route("/adolescentes")
def adolescentes():
    return render_template("calendario/adolescentes.html")


@main_blueprint.route("/adultos")
def adultos():
    return render_template("calendario/adultos.html")


@main_blueprint.route("/criancas")
def criancas():
    return render_template("calendario/criancas.html")


@main_blueprint.route("/gestantes")
def gestantes():
    return render_template("calendario/gestantes.html")


@main_blueprint.route("/idosos")
def idosos():
    return render_template("calendario/idosos.html")


@main_blueprint.route("/consulta_calendario", methods=["GET", "POST"])
def consulta_calendario():
    form = ConsultaCalendarioForm(request.form)

    if form.validate_on_submit():
        data_nascimento = form.data_nascimento.data
        is_gestante = form.is_gestante.data
        hoje = datetime.today().date()
        anos = relativedelta(hoje, data_nascimento).years

        # mensagem de alerta para as gestantes
        if is_gestante == '1':
            mensagem = '''
            Atenção!  De acordo com o Ministério da Saúde, há vacinas que gestantes não podem tomar. Verifique com seu médico.
            '''
            mensagem = Markup(mensagem)
            flash(mensagem, "danger")

        # criança - >=0 and 4 anos
        if anos >= 0 and anos <= 4:
            return render_template("calendario/criancas.html", is_gestante=is_gestante)

        if anos > 4 and anos < 9:
            # criança sem vacina - +4 e <9
            mensagem = '''
            Para essa faixa etária não há vacinas disponibilizadas obrigatórias de acordo com o ministério da Saúde.
            </br>
            Dicas:
            </br>
            - Consulte o posto de vacinação mais próximo para verificar se há campanhas locais de imunização.</br>
            -  Veja o calendário anterior se há alguma vacina faltante para imunização completa no quadro abaixo.            
            '''
            mensagem = Markup(mensagem)
            flash(mensagem, "warning")
            return render_template("calendario/criancas.html", is_gestante=is_gestante)

        # adolescente - 9 a 19 anos
        if anos >= 9 and anos <= 19:
            return render_template("calendario/adolescentes.html", is_gestante=is_gestante)

        # adulto - 20 A 59 anos
        if anos >= 20 and anos <= 59:
            return render_template("calendario/adultos.html", is_gestante=is_gestante)

        # idoso += 60
        if anos >= 60:
            return render_template("calendario/idosos.html", is_gestante=is_gestante)

        # Tabela
        # nome_grupo       caminho_pagina
        # adolescentes     calendario/adolescentes.html
        # criancas         calendario//criancas.html

        print(anos)

    return render_template("main/home.html", form=form)
