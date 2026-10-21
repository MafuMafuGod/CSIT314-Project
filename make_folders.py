import os

FILES = """
app.py
requirements.txt
README.md
.gitignore
entity/__init__.py
entity/database.py
entity/user_profile.py
entity/user_account.py
entity/company_profile.py
entity/activity_log.py
entity/project.py
entity/shortlist.py
entity/category.py
control/__init__.py
control/login_controller.py
control/user_account_controller.py
control/user_profile_controller.py
control/company_controller.py
control/portfolio_controller.py
control/customer_controller.py
control/platform_controller.py
boundary/__init__.py
boundary/helpers.py
boundary/login_pages.py
boundary/user_admin_pages.py
boundary/company_pages.py
boundary/portfolio_pages.py
boundary/customer_pages.py
boundary/platform_pages.py
templates/base.html
templates/login.html
templates/account.html
templates/confirm.html
templates/admin_accounts.html
templates/admin_account_form.html
templates/admin_account_view.html
templates/admin_profiles.html
templates/admin_profile_form.html
templates/admin_profile_view.html
templates/company_view.html
templates/company_form.html
templates/company_contact.html
templates/company_search.html
templates/portfolio_list.html
templates/project_form.html
templates/project_view.html
templates/interest.html
templates/idp_search.html
templates/idp_view.html
templates/shortlist.html
templates/platform_dashboard.html
templates/categories.html
templates/category_form.html
templates/category_view.html
templates/reports.html
static/style.css
tests/conftest.py
tests/test_portfolio.py
tests/test_other_stories.py
tests/test_pages.py
""".split()

for path in FILES:
    full = os.path.join("renovation_platform", path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "a").close
    print("created", full)