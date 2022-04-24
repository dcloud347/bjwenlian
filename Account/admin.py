from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from django.contrib import admin
from .models import SchoolAccount, UserAccount, ClubAccount,Participation


# Register your models here.
@admin.register(SchoolAccount)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'check')
    list_filter = ['check']


@admin.register(UserAccount)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('pk','username', 'grade', 'signature', 'phone', 'is_active', 'school', 'avatar')
    list_filter = ['grade', 'phone', 'clubs', 'is_active']
    filter_horizontal = ('clubs','liked_activity','liked_passage')


@admin.register(ClubAccount)
class ClubsAdmin(admin.ModelAdmin):
    list_display = ('name', 'simp_intro', 'full_intro', 'category', 'check', 'school', 'avatar')
    list_filter = ['name', 'category', 'check', 'school']
