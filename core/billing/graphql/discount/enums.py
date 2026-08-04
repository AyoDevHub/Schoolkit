import strawberry

from billing.models import ValueType, DiscountCategory


ValueTypeEnum = strawberry.enum(ValueType)
DiscountCategoryEnum = strawberry.enum(DiscountCategory)