import strawberry 

# -------- Class Level --------

@strawberry.input
class CreateClassLevelInput:
    school_id: strawberry.ID
    name: str


@strawberry.input
class UpdateClassLevelInput:
    class_level_id: strawberry.ID
    name: str | None= None


# -------- Class Arm --------
@strawberry.input
class CreateClassArmInput:
    class_level_id: strawberry.ID
    name: str


@strawberry.input
class UpdateClassArmInput:
    class_arm_id: strawberry.ID
    name: str