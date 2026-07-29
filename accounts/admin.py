from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Rol", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Rol", {"fields": ("role",)}),)
    list_display = UserAdmin.list_display + ("role",)


admin.site.register(Usuario, UsuarioAdmin)
