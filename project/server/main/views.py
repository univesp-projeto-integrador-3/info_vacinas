# project/server/main/views.py


from flask import Blueprint, flash, redirect, render_template, request, url_for
from project.server.main.forms import ConsultaCalendarioForm

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def home():
    return render_template("main/home.html")


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
        nome = form.nome.data
        data_nascimento = form.data_nascimento.data
        is_gestante = form.is_gestante.data

        print(nome, data_nascimento, is_gestante)

        # db.session.add(user)

        flash("Direcionando para o calendário de idosos.", "success")
        return redirect(url_for("main.idosos"))

    return render_template("main/home.html", form=form)
