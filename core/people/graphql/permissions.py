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
# Student Permissions
# -------------------------------------------------------------------------

class CanCreateStudent(IsAdministrator):
    message = "You do not have permission to create students."


class CanUpdateStudent(IsAdministrator):
    message = "You do not have permission to update students."


class CanActivateStudent(IsAdministrator):
    message = "You do not have permission to activate students."


class CanDeactivateStudent(IsAdministrator):
    message = "You do not have permission to deactivate students."


class CanViewStudents(IsAdministrator):
    message = "You do not have permission to view students."


# -------------------------------------------------------------------------
# Guardian Permissions
# -------------------------------------------------------------------------

class CanCreateGuardian(IsAdministrator):
    message = "You do not have permission to create guardians."


class CanUpdateGuardian(IsAdministrator):
    message = "You do not have permission to update guardians."


class CanActivateGuardian(IsAdministrator):
    message = "You do not have permission to activate guardians."


class CanDeactivateGuardian(IsAdministrator):
    message = "You do not have permission to deactivate guardians."


class CanViewGuardians(IsAdministrator):
    message = "You do not have permission to view guardians."


# -------------------------------------------------------------------------
# Student Guardian Permissions
# -------------------------------------------------------------------------

class CanCreateStudentGuardian(IsAdministrator):
    message = "You do not have permission to create student guardian relationships."


class CanUpdateStudentGuardian(IsAdministrator):
    message = "You do not have permission to update student guardian relationships."


class CanActivateStudentGuardian(IsAdministrator):
    message = "You do not have permission to activate student guardian relationships."


class CanDeactivateStudentGuardian(IsAdministrator):
    message = "You do not have permission to deactivate student guardian relationships."


class CanViewStudentGuardians(IsAdministrator):
    message =  "You do not have permission to view student guardian relationships."



# -------------------------------------------------------------------------
# Enrollment Permissions
# -------------------------------------------------------------------------

class CanCreateEnrollment(IsAdministrator):
    message = "You do not have permission to create enrollments."


class CanUpdateEnrollment(IsAdministrator):
    message = "You do not have permission to update enrollments."


class CanActivateEnrollment(IsAdministrator):
    message = "You do not have permission to activate enrollments."


class CanDeactivateEnrollment(IsAdministrator):
    message = "You do not have permission to deactivate enrollments."


class CanWithdrawStudent(IsAdministrator):
    message = "You do not have permission to withdraw students."


class CanPromoteStudent(IsAdministrator):
    message = "You do not have permission to promote students."


class CanTransferStudent(IsAdministrator):
    message = "You do not have permission to transfer students."


class CanViewEnrollments(IsAdministrator):
    message = "You do not have permission to view enrollments."