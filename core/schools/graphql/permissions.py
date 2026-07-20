from strawberry.permission import BasePermission
from strawberry.types import Info



# -------------------------------------------------------------------------
# Base Permissions
# -------------------------------------------------------------------------

class IsAdministrator(BasePermission):

    """
    Base permission for administrator-only actions.
    """

    def has_permission(
        self,
        source,
        info: Info,
        **kwargs,
    ) -> bool:

        user = info.context.user

        return (
            user is not None
            and user.is_administrator
        )

    

# -------------------------------------------------------------------------
# School Permissions
# -------------------------------------------------------------------------

class CanCreateSchool(IsAdministrator):
    # Error message
    message = "You do not have permission to create schools."


class CanUpdateSchool(IsAdministrator):

    # Error message
    message = "You do not have permission to update schools."


class CanActivateSchool(IsAdministrator):
    # Error message
    message = "You do not have permission to activate schools."


class CanDeactivateSchool(IsAdministrator):
    # Error message
    message = "You do not have permission to deactivate schools."
    

class CanViewSchools(IsAdministrator):
    # Error message
    message = "You dont have the permission to view schools."



# -------------------------------------------------------------------------
# Academic Session Permissions
# -------------------------------------------------------------------------

class CanCreateAcademicSession(IsAdministrator):
    message = "You do not have permission to create academic sessions."


class CanUpdateAcademicSession(IsAdministrator):
    message = "You do not have permission to update academic sessions."


class CanActivateAcademicSession(IsAdministrator):
    message = "You do not have permission to activate academic sessions."


class CanDeactivateAcademicSession(IsAdministrator):
    message = "You do not have permission to deactivate academic sessions."


class CanViewAcademicSessions(IsAdministrator):
    message = "You do not have permission to view academic sessions."


# -------------------------------------------------------------------------
# Academic Term Permissions
# -------------------------------------------------------------------------

class CanCreateAcademicTerm(IsAdministrator):
    message = "You do not have permission to create academic terms."


class CanUpdateAcademicTerm(IsAdministrator):
    message = "You do not have permission to update academic terms."


class CanActivateAcademicTerm(IsAdministrator):
    message = "You do not have permission to activate academic terms."


class CanDeactivateAcademicTerm(IsAdministrator):
    message = "You do not have permission to deactivate academic terms."


class CanViewAcademicTerms(IsAdministrator):
    message = "You dont have permissionn to perform this action."




# -------------------------------------------------------------------------
# School Class level Permissions
# -------------------------------------------------------------------------

class CanCreateSchoolClassLevel(IsAdministrator):
    message= "You do not have permission to create a class levels."


class CanUpdateSchoolClassLevel(IsAdministrator):
    message= "You do not have permission to update a class level."


class CanViewSchoolClassLevel(IsAdministrator):
    message= "You do not have permission to perform this action."



# -------------------------------------------------------------------------
# School Class Arm Permissions
# -------------------------------------------------------------------------

class CanCreateSchoolClassArm(IsAdministrator):
    message= "You do not have permission to create a class arms."


class CanUpdateSchoolClassArm(IsAdministrator):
    message= "You do not have permission to update a class arm."


class CanViewSchoolClassArm(IsAdministrator):
    message= "You do not have permission to perform this action."



# -------------------------------------------------------------------------
# Subject Permissions
# -------------------------------------------------------------------------

class CanCreateSubject(IsAdministrator):
    message = "You do not have permission to create subjects."


class CanUpdateSubject(IsAdministrator):
    message = "You do not have permission to update subjects."


class CanViewSubjects(IsAdministrator):
    message = "You do not have permission to view subjects."