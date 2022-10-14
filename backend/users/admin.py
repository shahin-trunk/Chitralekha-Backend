from django.contrib.auth.models import Group
from .models import User
from organization.models import *
from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportActionModelAdmin
from import_export.widgets import ForeignKeyWidget

# Register your models here.


class UserResource(resources.ModelResource):
    class Meta:
        import_id_fields = ("id",)
        # exclude = ('datasetbase_ptr',)
        model = User


class UserAdmin(ImportExportActionModelAdmin):
    resource_class = UserResource


admin.site.register(User)

# admin.site.register(UserAdmin)

admin.site.unregister(Group)
