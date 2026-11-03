"""Placeholder pages (NOT part of any use case yet).
They only exist so the links in the templates work. Each one gets replaced
with real Boundary / Control / Entity code in its own use case."""
from flask import Blueprint, render_template, render_template_string, flash, redirect, url_for

COMING_SOON = """{% extends "base.html" %}
{% block title %}{{ name }} | 4RENO{% endblock %}
{% block content %}<h1>{{ name }}</h1><div class="banner info">Coming soon.</div>{% endblock %}"""

home = Blueprint("home", __name__)
search_shortlist = Blueprint("search_shortlist", __name__)
save_favourite = Blueprint("save_favourite", __name__)


@home.route("/home")
def displayHome():
    return render_template("home.html", categories=[], featured=[])


@search_shortlist.route("/shortlist")
def shortlistPage():
    return render_template_string(COMING_SOON, name="My Shortlist", active="shortlist")


@save_favourite.route("/idp/<int:idpID>/save", methods=["POST"])
def saveRoute(idpID: int):
    """Placeholder for #34 Save IDP to shortlist, so the button on the #33 details page works."""
    flash("Saving to your shortlist is coming soon.", "info")
    return redirect(url_for("view_idp.viewIdpPage", idpID=idpID))
