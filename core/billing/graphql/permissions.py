from strawberry.permission import BasePermission
from strawberry.types import Info



# -------------------------------------------------------------------------
# Base Permissions
# -------------------------------------------------------------------------

class IsFinanceOfficer(BasePermission):

    def has_permission(
        self,
        source,
        info: Info,
        **kwargs,
    ) -> bool:

        user = info.context.user

        return (
            user is not None
            and (
                user.is_administrator
                or user.is_bursar
            )
        )          
# -------------------------------------------------------------------------
# Fee Item Permissions
# -------------------------------------------------------------------------

class CanCreateFeeItem(IsFinanceOfficer):
    message = "You do not have permission to create fee items."


class CanUpdateFeeItem(IsFinanceOfficer):
    message = "You do not have permission to update fee items."


class CanActivateFeeItem(IsFinanceOfficer):
    message = "You do not have permission to activate fee items."


class CanDeactivateFeeItem(IsFinanceOfficer):
    message = "You do not have permission to deactivate fee items."


class CanViewFeeItem(IsFinanceOfficer):
    message = "You do not have permission to view fee items."


# -------------------------------------------------------------------------
# Fee Schedule Permissions
# -------------------------------------------------------------------------

class CanCreateFeeSchedule(IsFinanceOfficer):
    message = "You do not have permission to create fee schedules."


class CanUpdateFeeSchedule(IsFinanceOfficer):
    message = "You do not have permission to update fee schedules."


class CanActivateFeeSchedule(IsFinanceOfficer):
    message = "You do not have permission to activate fee schedules."


class CanDeactivateFeeSchedule(IsFinanceOfficer):
    message = "You do not have permission to deactivate fee schedules."


class CanViewFeeSchedule(IsFinanceOfficer):
    message = "You do not have permission to view fee schedules."


# -------------------------------------------------------------------------
# Fee Schedule item Permissions
# -------------------------------------------------------------------------

class CanCreateFeeScheduleItem(IsFinanceOfficer):
    message = "You do not have permission to create fee schedule items."


class CanUpdateFeeScheduleItem(IsFinanceOfficer):
    message = "You do not have permission to update fee schedule items."


class CanDeleteFeeScheduleItem(IsFinanceOfficer):
    message = "You do not have permission to delete fee schedule items."


class CanViewFeeScheduleItem(IsFinanceOfficer):
    message = "You do not have permission to view fee schedule items."


# -------------------------------------------------------------------------
# Discount Permissions
# -------------------------------------------------------------------------

class CanCreateDiscount(IsFinanceOfficer):
    message = "You do not have permission to create discounts."


class CanUpdateDiscount(IsFinanceOfficer):
    message = "You do not have permission to update discounts."


class CanActivateDiscount(IsFinanceOfficer):
    message = "You do not have permission to activate discounts."


class CanDeactivateDiscount(IsFinanceOfficer):
    message = "You do not have permission to deactivate discounts."


class CanViewDiscount(IsFinanceOfficer):
    message = "You do not have permission to view discounts."