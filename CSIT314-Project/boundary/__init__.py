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
from boundary.company_profile_page import company_profile
from boundary.manage_contact_info_page import manage_contact_info
from boundary.search_company_profiles_page import search_company_profiles
from boundary.portfolio_page import portfolio
from boundary.create_portfolio_page import create_portfolio
from boundary.view_portfolio_page import view_portfolio
from boundary.update_portfolio_page import update_portfolio
from boundary.delete_portfolio_page import delete_portfolio
from boundary.save_idp_page import save_favourite
from boundary.search_shortlist_page import search_shortlist
from boundary.view_shortlisted_idp_page import view_shortlisted
from boundary.placeholder_pages import home

ALL_BLUEPRINTS = (login, logout, create_account, user_management, update_account, suspend_account,
                  create_profile, view_profile, update_profile, suspend_profile,
                  idp_interest, search_idp, view_idp, company_profile, manage_contact_info, search_company_profiles,
                  portfolio, create_portfolio, view_portfolio, update_portfolio, delete_portfolio, home, save_favourite, search_shortlist, view_shortlisted)
