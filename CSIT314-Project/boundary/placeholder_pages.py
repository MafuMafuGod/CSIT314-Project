"""Placeholder pages (NOT part of any use case yet).
They only exist so the links in the templates work. Each one gets replaced
with real Boundary / Control / Entity code in its own use case."""
from flask import Blueprint, render_template

home = Blueprint("home", __name__)


@home.route("/home")
def displayHome():
    return render_template("home.html", categories=[], featured=[])
