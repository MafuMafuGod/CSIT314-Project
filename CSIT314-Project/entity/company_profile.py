"""«Entity» CompanyProfile — used by #09 Create, #10 View, #11 Update company profile,
#12 Manage contact information and #13 Search company profiles.
One company profile per Interior Designer (ID). Field names follow Dominic's design
(companyName, description, businessEmail, businessPhone, businessAddress, website)."""
from typing import Optional


class CompanyProfile:
    #An Interior Designer's company information, shown to customers.

    _profiles = []                      # stand-in for the database table

    def __init__(self, designerU: str, companyName: str, description: str,
                 businessEmail: str, businessPhone: str, businessAddress: str,
                 website: str = "", instagram: str = "", facebook: str = "",
                 linkedin: str = "") -> None:
        self._designerU = designerU      # the ID's username (email) - one profile each
        self._companyName = companyName
        self._description = description
        self._businessEmail = businessEmail
        self._businessPhone = businessPhone
        self._businessAddress = businessAddress
        self._website = website          # optional
        self._instagram = instagram      # optional social media (#12)
        self._facebook = facebook
        self._linkedin = linkedin

    # ---- private helpers ---------------------------------------------------
    @classmethod
    def _findProfile(cls, designerU: str) -> Optional["CompanyProfile"]:
        for profile in cls._profiles:
            if profile._designerU == designerU:
                return profile
        return None

    def _toDict(self) -> dict:
        return {"companyName": self._companyName, "description": self._description,
                "businessEmail": self._businessEmail, "businessPhone": self._businessPhone,
                "businessAddress": self._businessAddress, "website": self._website,
                "instagram": self._instagram, "facebook": self._facebook, "linkedin": self._linkedin}

    # ---- #09 Create company profile -----------------------------------------
    @classmethod
    def profileExists(cls, designerU: str) -> bool:
        # 09 precondition check: does this ID already have a company profile?
        return cls._findProfile(designerU) is not None

    @classmethod
    def createProfile(cls, designerU: str, companyName: str, description: str,
                      businessEmail: str, businessPhone: str, businessAddress: str,
                      website: str = "") -> bool:
        #09 step 3: save the new company profile. 

        cls._profiles.append(CompanyProfile(designerU, companyName, description, businessEmail,
                                            businessPhone, businessAddress, website))
        return True

    # ---- #10 View company profile / #11 step 2 -------------------------------
    @classmethod
    def getProfile(cls, designerU: str) -> dict:
        """#10 step 2: return the ID's company profile ({} if not created, alt 2a)."""
        profile = cls._findProfile(designerU)
        return profile._toDict() if profile else {}

    # ---- #11 Update company information -------------------------------------
    @classmethod
    def updateProfile(cls, designerU: str, companyName: str, description: str,
                      businessEmail: str, businessPhone: str, businessAddress: str,
                      website: str = "") -> bool:
        """#11 step 3: save the changed company information. False if no profile exists."""
        profile = cls._findProfile(designerU)
        if profile is None:
            return False
        profile._companyName = companyName
        profile._description = description
        profile._businessEmail = businessEmail
        profile._businessPhone = businessPhone
        profile._businessAddress = businessAddress
        profile._website = website
        return True


    # ---- #12 Manage contact information ------------------------------------
    @classmethod
    def updateContactInfo(cls, designerU: str, businessEmail: str, businessPhone: str,
                          businessAddress: str, website: str, instagram: str, facebook: str,
                          linkedin: str) -> bool:
        """#12 step 3: save only the contact fields. False if no profile exists."""
        profile = cls._findProfile(designerU)
        if profile is None:
            return False
        profile._businessEmail = businessEmail
        profile._businessPhone = businessPhone
        profile._businessAddress = businessAddress
        profile._website = website
        profile._instagram = instagram
        profile._facebook = facebook
        profile._linkedin = linkedin
        return True

    # ---- #13 Search company profiles ----------------------------------------
    @classmethod
    def searchProfiles(cls, keyword: str) -> list:
        """#13: profiles whose name or public details contain the keyword (not case-sensitive),
        A-Z by company name. [] if nothing matches."""
        keyword = keyword.casefold()
        matches = [p._toDict() for p in cls._profiles
                   if keyword in " ".join(p._toDict().values()).casefold()]
        return sorted(matches, key=lambda row: row["companyName"].casefold())


# Sample data: designer@4reno.com starts WITHOUT a profile so the demo can show
# #09 Create -> #10 View -> #11 Update in order. Two other designers' profiles are
# included so #13 Search has something to find.
CompanyProfile._profiles = [
    CompanyProfile("formfield@4reno.com", "Form & Field Interiors", "Thoughtful spaces for everyday living.",
                   "hello@formandfield.sg", "+65 6123 4567", "21 Tanjong Pagar Road, Singapore 088444",
                   "https://formandfield.sg", "@formandfield", "Form & Field Interiors", "Form & Field Interiors"),
    CompanyProfile("nookstudio@4reno.com", "Nook Studio", "Compact HDB and condo makeovers with clever storage.",
                   "hi@nookstudio.sg", "+65 6789 0123", "8 Ubi Road 2, Singapore 408538",
                   instagram="@nookstudio.sg"),
]
