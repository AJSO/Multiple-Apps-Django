from django.contrib import admin
from .models import Profile, ProfilePic

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']

    class Meta:
        model = Profile

admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfilePic)