"""User profiles shown on the pages (Boundary display data).
One place to add or rename a profile: the key is what is stored in UserAccount
and the session, the value is what the user sees."""

PROFILE_LABELS = {
    "customer": "Customer",
    "designer": "Interior Designer",
    "admin": "User Admin",
    "platform": "Platform Management",
}

VALID_PROFILES = list(PROFILE_LABELS)
