from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('privacy', 'headline', 'skills', 'education', 'work_experience',
              'portfolio_link', 'linkedin_link', 'github_link', 'other_links', 'location')


@admin.action(description='Grant staff status')
def make_staff(modeladmin, request, queryset):
    updated = queryset.update(is_staff=True)
    modeladmin.message_user(request, f"Marked {updated} user(s) as staff.", messages.SUCCESS)


@admin.action(description='Revoke staff status')
def remove_staff(modeladmin, request, queryset):
    updated = queryset.update(is_staff=False)
    modeladmin.message_user(request, f"Removed staff from {updated} user(s).", messages.SUCCESS)


@admin.action(description='Activate selected users')
def activate_users(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(request, f"Activated {updated} user(s).", messages.SUCCESS)


@admin.action(description='Deactivate selected users')
def deactivate_users(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    modeladmin.message_user(request, f"Deactivated {updated} user(s).", messages.SUCCESS)


class CustomUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'get_role', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'profile__role')
    actions = [make_staff, remove_staff, activate_users, deactivate_users]

    def get_role(self, obj):
        try:
            return obj.profile.role
        except Profile.DoesNotExist:
            return ''
    get_role.short_description = 'Role'


# Unregister the original User admin and register the new one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'headline', 'role', 'privacy', 'company', 'location')
    search_fields = ('user__username', 'user__email', 'headline', 'skills', 'location', 'company')
    list_filter = ('role', 'privacy')
    readonly_fields = ('user',)

    fieldsets = (
        ('User Information', {
            'fields': ('user', 'privacy', 'role', 'company', 'location')
        }),
        ('Professional Profile', {
            'fields': ('headline', 'skills', 'education', 'work_experience')
        }),
        ('Links', {
            'fields': ('portfolio_link', 'linkedin_link', 'github_link', 'other_links')
        }),
    )

# Register ProfileAdmin safely in case admin.autodiscover runs multiple times
from django.contrib.admin.sites import AlreadyRegistered
try:
    admin.site.register(Profile, ProfileAdmin)
except AlreadyRegistered:
    # If it's already registered (e.g., imported twice during checks), unregister and reregister
    try:
        admin.site.unregister(Profile)
    except Exception:
        pass
    admin.site.register(Profile, ProfileAdmin)
