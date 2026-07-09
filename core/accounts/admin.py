from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User
from accounts.forms import UserChangeForm, UserCreationForm

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    
    list_display = (
        'email',
        'full_name',
        'role',
        'school',
        'is_staff',
        'is_active',
    )
    
    list_filter = (
        'role',
        'is_active',
        'school',
    )
    
    search_fields = (
        'email',
        'first_name',
        'last_name',
    )
    
    ordering = ('email',)
    
    fieldsets = (
        (None, {
            "fields": (
                'email',
                'password',
            ),
        }),
        
        ('Personal', {
            "fields": (
                'first_name',
                'last_name',
                'phone_number',
            )
        }),
        
        ('School', {
            "fields": (
                'school',
                'role',
            )
        }),
        
        ('Permissions', {
            "fields": (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        
        ('Audit Information', {
            "fields": (
                "last_login",
                "created_at",
                "updated_at",
                )
        })
    )
    
    
    add_fieldsets = (
    (
        None,
        {
            "classes": ("wide",),
            "fields": (
                "email",
                "first_name",
                "last_name",
                "role",
                "school",
                "password1",
                "password2",
            ),
        },
    ),
)
    
    readonly_fields = (
        "last_login",
        "created_at",
        "updated_at",
    )