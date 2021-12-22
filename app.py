from flask import Flask, render_template, request, abort
from flask.helpers import url_for
from werkzeug.utils import redirect
from requests import get
import re
import json


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    data = get("https://api.elpais.com/ws/LoteriaNavidadPremiados?n=resumen")
    data = json.loads("{" + data.content.decode().split("{", 1)[1].split("}")[0] + "}")
    premios = {}

    for val in data:
        if data[val] == -1:
            data[val] = " - "
        if "numero" in val:
            newval = {
                "numero1": "Premio Gordo",
                "numero2": "Segundo premio",
                "numero3": "Tercer premio",
                "numero4": "Cuarto premio",
                "numero5": "Cuarto premio",
                "numero6": "Quinto premio",
                "numero7": "Quinto premio",
                "numero8": "Quinto premio",
                "numero9": "Quinto premio",
                "numero10": "Quinto premio",
                "numero11": "Quinto premio",
                "numero12": "Quinto premio",
                "numero13": "Quinto premio",
            }[val]
            # breakpoint()

            if newval in premios:
                premios[newval].append(data[val])
            else:
                premios.update({newval: [data[val]]})

    return render_template("index.html", premios=premios)


@app.route("/comprobar", methods=["GET", "POST"])
def comprobar():
    if request.method == "POST":
        number = request.form.get("number")
        if not number:
            abort(400)

        test = get("https://api.elpais.com/ws/LoteriaNavidadPremiados?n="+number)
        answer_json = json.loads("{" + test.content.decode().split('{', 1)[1].split('}')[0] + "}")
        
        if answer_json["premio"] == 0:
            response = get("https://api.elpais.com/ws/LoteriaNavidadPremiados?s=1")
            is_running = json.loads(
                "{" + response.content.decode().split("{", 1)[1].split("}")[0] + "}"
            )["status"]
            return render_template(
                "not_yet.html", numero=answer_json["numero"], is_running=is_running
            )

        return render_template(
            "winner.html", numero=answer_json["numero"], premio=answer_json["premio"]
        )

    abort(403)
