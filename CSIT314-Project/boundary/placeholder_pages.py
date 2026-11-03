"""Placeholder pages (NOT part of any use case yet).
They only exist so the navbar links in base.html work. Each one gets replaced
with real Boundary / Control / Entity code in its own use case."""
from flask import Blueprint, render_template, render_template_string

COMING_SOON = """{% extends "base.html" %}
{% block title %}{{ name }} | 4RENO{% endblock %}
{% block content %}<h1>{{ name }}</h1><div class="banner info">Coming soon.</div>{% endblock %}"""

home = Blueprint("home", __name__)
search_shortlist = Blueprint("search_shortlist", __name__)
view_idp = Blueprint("view_idp", __name__)


@home.route("/home")
def displayHome():
    return render_template("home.html", categories=[], featured=[])


@search_shortlist.route("/shortlist")
def shortlistPage():
    return render_template_string(COMING_SOON, name="My Shortlist", active="shortlist")


@view_idp.route("/idp/<int:idpID>")
def viewIdpPage(idpID: int):
    """Placeholder for #33 View IDP details, so the search result "View Details" buttons work."""
    return render_template_string(COMING_SOON, name="IDP Details", active="search")
