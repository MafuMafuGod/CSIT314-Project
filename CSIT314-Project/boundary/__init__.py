"""«Boundary» layer: pages, routes and INPUT VALIDATION. Imports only from control/."""
from boundary.user_login_page import login
from boundary.user_logout_page import logout
from boundary.create_user_account_page import create_account
from boundary.view_user_account_page import user_management
from boundary.idp_interest_page import idp_interest
from boundary.search_idp_page import search_idp
from boundary.placeholder_pages import home, search_shortlist, view_idp

ALL_BLUEPRINTS = (login, logout, create_account, user_management, idp_interest, search_idp,
                  home, search_shortlist, view_idp)
