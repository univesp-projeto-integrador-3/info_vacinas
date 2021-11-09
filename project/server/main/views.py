# project/server/main/views.py


from flask import render_template, Blueprint


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def home():
    return render_template("main/home.html")


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")


@main_blueprint.route("/adolescentes/")
def adolescentes():
    return render_template("calendario/adolescentes.html")


@main_blueprint.route("/adultos/")
def adultos():
    return render_template("calendario/adultos.html")


@main_blueprint.route("/criancas/")
def criancas():
    return render_template("calendario/criancas.html")


@main_blueprint.route("/gestantes/")
def gestantes():
    return render_template("calendario/gestantes.html")


@main_blueprint.route("/idosos/")
def idosos():
    return render_template("calendario/idosos.html")        