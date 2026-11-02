"""Placeholder pages (NOT part of any use case yet).
They only exist so the navbar links in base.html work. Each one gets replaced
with real Boundary / Control / Entity code in its own use case."""
from flask import Blueprint, render_template, render_template_string

COMING_SOON = """{% extends "base.html" %}
{% block title %}{{ name }} | 4RENO{% endblock %}
{% block content %}<h1>{{ name }}</h1><div class="banner info">Coming soon.</div>{% endblock %}"""

home = Blueprint("home", __name__)
search_idp = Blueprint("search_idp", __name__)
search_shortlist = Blueprint("search_shortlist", __name__)


@home.route("/home")
def displayHome():
    return render_template("home.html", categories=[], featured=[])


@search_idp.route("/search")
def searchPage():
    return render_template_string(COMING_SOON, name="Interior Designers", active="search")


@search_shortlist.route("/shortlist")
def shortlistPage():
    return render_template_string(COMING_SOON, name="My Shortlist", active="shortlist")
