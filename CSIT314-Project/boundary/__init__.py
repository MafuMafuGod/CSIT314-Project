"""«Boundary» layer: pages, routes and INPUT VALIDATION. Imports only from control/."""
from boundary.user_login_page import login
from boundary.user_logout_page import logout
from boundary.create_user_account_page import create_account
from boundary.view_user_account_page import user_management
from boundary.update_user_account_page import update_account
from boundary.suspend_user_account_page import suspend_account
from boundary.create_user_profile_page import create_profile
from boundary.view_user_profile_page import view_profile
from boundary.update_user_profile_page import update_profile
from boundary.suspend_user_profile_page import suspend_profile
from boundary.idp_interest_page import idp_interest
from boundary.search_idp_page import search_idp
from boundary.view_idp_page import view_idp
from boundary.placeholder_pages import home, search_shortlist, save_favourite

ALL_BLUEPRINTS = (login, logout, create_account, user_management, update_account, suspend_account,
                  create_profile, view_profile, update_profile, suspend_profile,
                  idp_interest, search_idp, view_idp, home, search_shortlist, save_favourite)
