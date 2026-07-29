from django.contrib import admin

from .models import Liga


@admin.register(Liga)
class LigaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "codigo", "admin", "activa", "creada_en"]
    readonly_fields = ["codigo"]
