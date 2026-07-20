from django.contrib import admin

from schools.models import ClassLevel, ClassArm


class ClassArmInline(admin.TabularInline):
    model = ClassArm
    extra = 1
    fields = ("name",)

@admin.register(ClassLevel)
class ClassLevelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "school",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "school",
    )

    search_fields = (
        "name",
        "school__name",
    )

    ordering = (
        "school__name",
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = [
        ClassArmInline,
    ]


@admin.register(ClassArm)
class ClassArmAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "level",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "level",
        "level__school",
    )

    search_fields = (
        "name",
        "level__name",
        "level__school__name",
    )

    ordering = (
        "level__school__name",
        "level__name",
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )