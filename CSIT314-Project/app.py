"""
4RENO - Interior Design Project (IDP) platform

Use cases in this code:
  #06 User Login  #07 User Logout  #31 Customer Login  #70 Platform Admin Login
  #09 Create  #10 View  #11 Update  Company Profile (Matthew)
  #32 Search IDPs  #33 View IDP Details
  #40 / #41 IDP view and shortlist count (Matthew)
  #42 Create  #43 View  #44 Update  #45 Suspend  #46 Search  User Account
  #47 Create  #48 View  #49 Update  #50 Suspend  #51 Search  User Profile

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
from boundary.profiles import getProfileLabels
from control import SessionCheckController

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"


# Infrastructure (not part of the BCE diagrams): session check, login guard, admin guard,
# designer guard + CSRF protection

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
    return {"profileLabels": getProfileLabels()}


@app.before_request
def endSuspendedSessions():
    """#45 step 5 / #50 step 4: a user who was suspended (or whose profile was suspended)
    while logged in is signed out on their next page load."""
    if session.get("u") and SessionCheckController().isSessionBlocked(session["u"], session.get("profile", "")):
        session.clear()
        flash("Your account has been suspended. Please contact the User Admin.", "err")
        return redirect(url_for("login.loginPage"))


@app.before_request
def requireLogin():
    """Precondition for #07: only a logged-in user can log out."""
    if request.path == "/logout" and not session.get("u"):
        return redirect(url_for("login.loginPage"))


@app.before_request
def requireAdmin():
    """Precondition for #42-#51 (and #45 6b / #50 2a "no permission"): only a logged-in
    User Admin may open /admin pages."""
    if request.path.startswith("/admin") and session.get("profile") != "admin":
        flash("You do not have permission to access User Management.", "err")
        return redirect(url_for("home.displayHome"))


@app.before_request
def requireDesigner():
    """Precondition for #09-#11 and #40/#41: only a logged-in ID may open /designer pages."""
    if request.path.startswith("/designer"):
        if not session.get("u"):
            return redirect(url_for("login.loginPage"))
        if session.get("profile") != "designer":
            flash("Only Interior Designers can access this page.", "err")
            return redirect(url_for("home.displayHome"))


@app.before_request
def check_csrf():
    if request.method == "POST" and request.form.get("csrf_token") != session.get("csrf"):
        abort(400, "Invalid CSRF token")


for bp in ALL_BLUEPRINTS:
    app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)
