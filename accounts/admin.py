from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('privacy', 'headline', 'skills', 'education', 'work_experience', 
              'portfolio_link', 'linkedin_link', 'github_link', 'other_links')
    readonly_fields = ()

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_headline')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    def get_headline(self, obj):
        try:
            return obj.profile.headline
        except Profile.DoesNotExist:
            return "No profile"
    get_headline.short_description = 'Professional Headline'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'headline', 'privacy')
    list_filter = ('privacy',)
    search_fields = ('user__username', 'user__email', 'headline', 'skills')
    readonly_fields = ('user',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'privacy')
        }),
        ('Professional Profile', {
            'fields': ('headline', 'skills', 'education', 'work_experience')
        }),
        ('Links', {
            'fields': ('portfolio_link', 'linkedin_link', 'github_link', 'other_links')
        }),
    )
