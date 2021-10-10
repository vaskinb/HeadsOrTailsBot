from django.contrib import admin
from .forms import ProfileForm
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'name', 'balance')
    form = ProfileForm
