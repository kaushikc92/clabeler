from django.contrib import admin

from models import Project
from models import Assignment
from models import HIT
from models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    fields = ('user','location','age', 'gender', 'career', 'approval_rate', 'approval_HIT_number', )

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Project)
admin.site.register(HIT)
admin.site.register(Assignment)
