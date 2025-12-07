from django.contrib import admin
from django import forms
from .models import Series, Episode
from core.utils.bunny import upload_to_bunny
import os
import tempfile


class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1
    ordering = ("season", "number")
    fields = ("season", "number", "title", "video_path")


class SeriesAdminForm(forms.ModelForm):
    cover_upload = forms.FileField(required=False, help_text="Envie a capa; salvaremos no Bunny e preencheremos cover_url.")

    class Meta:
        model = Series
        fields = "__all__"


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    form = SeriesAdminForm
    list_display = ("id", "title", "year", "category")
    list_filter = ("year", "category")
    search_fields = ("title", "description")
    inlines = [EpisodeInline]
    fieldsets = (
        (None, {"fields": ("title", "description", "year", "category")}),
        ("Mídia", {"fields": ("cover_url", "cover_upload", "trailer_url")}),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        f = form.cleaned_data.get("cover_upload")
        if f:
            name, ext = os.path.splitext(f.name)
            remote = f"covers/series/{obj.id}{ext.lower()}"
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(f.read())
                tmp.flush()
                public_url = upload_to_bunny(tmp.name, remote)
            obj.cover_url = public_url
            obj.save(update_fields=["cover_url"]) 


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("id", "series", "season", "number", "title", "created_at")
    list_filter = ("series", "season")
    search_fields = ("title",)
    ordering = ("series", "season", "number")