"""
4RENO - Use Case #06: User Login
       Use Case #07: User Logout
       Use Case #42: Create User Account
       Use Case #43: View User Account
       Use Case #40: Track and display IDP view count       (Matthew)
       Use Case #41: Track and display IDP shortlist count  (Matthew)

Project layout (one file per BCE class / page):
  entity/     «Entity»   classes - own the data, answer questions that need stored data
  control/    «Control»  classes - one per use case, coordinate Boundary -> Entity
  boundary/   «Boundary» pages   - routes, display functions, INPUT VALIDATION (no class)
  templates/  HTML templates used by the Boundary

BCE rules for all use cases (current and future):
  1. Boundary validates the input itself (empty fields, format, allowed values).
  2. Control only coordinates: it calls the Entity and returns the result.
  3. Entity answers anything that needs stored data (credentials, duplicates).
  4. Boundary -> Control -> Entity only. Boundary never imports from entity/.

Run:  python app.py
Demo accounts (u / p / profile):
  customer@4reno.com  / password123 / customer
  designer@4reno.com  / design123   / designer
  admin@4reno.com     / admin123    / admin
  platform@4reno.com  / platform123 / platform
"""


import secrets

from flask import Flask, request, session, abort, flash, redirect, url_for

from boundary import ALL_BLUEPRINTS
from boundary.profiles import PROFILE_LABELS

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"


# Infrastructure (not part of the BCE diagrams): login guard, admin guard, designer guard + CSRF protection

@app.context_processor
def inject_csrf():
    def csrf_token():
        if "csrf" not in session:
            session["csrf"] = secrets.token_hex(16)
        return session["csrf"]
    return {"csrf_token": csrf_token}


@app.context_processor
def inject_profile_labels():
    """Lets every template show "Interior Designer" instead of "designer"."""
    return {"profileLabels": PROFILE_LABELS}


@app.before_request
def requireLogin():
    """Precondition for #07: only a logged-in user can log out."""
    if request.path == "/logout" and not session.get("u"):
        return redirect(url_for("login.loginPage"))


@app.before_request
def requireAdmin():
    """Precondition for #42/#43: only a logged-in User Admin may open /admin pages."""
    if request.path.startswith("/admin") and session.get("profile") != "admin":
        flash("You do not have permission to access User Management.", "err")
        return redirect(url_for("home.displayHome"))


@app.before_request
def requireDesigner():
    """Precondition for #40/#41: only a logged-in ID may open the IDP Interest page."""
    if request.path.startswith("/designer/interest"):
        if not session.get("u"):
            return redirect(url_for("login.loginPage"))
        if session.get("profile") != "designer":
            flash("Only Interior Designers can view IDP interest.", "err")
            return redirect(url_for("home.displayHome"))


@app.before_request
def check_csrf():
    if request.method == "POST" and request.form.get("csrf_token") != session.get("csrf"):
        abort(400, "Invalid CSRF token")


for bp in ALL_BLUEPRINTS:
    app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)
