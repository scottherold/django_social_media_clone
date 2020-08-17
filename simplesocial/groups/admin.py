from django.contrib import admin
from . import models

class GroupMemberInLine(admin.TabularInline):
    """A class to register the GroupMember model."""
    model = models.GroupMember

# Register your models here.
admin.site.register(models.Group)