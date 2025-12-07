from django.contrib import admin
from django import forms
from .models import Category, Movie, HomeBanner
from core.utils.bunny import upload_to_bunny
import os


class MovieAdminForm(forms.ModelForm):
    cover_upload = forms.FileField(required=False, help_text="Envie a imagem; salvaremos no Bunny e preencheremos cover_url.")

    class Meta:
        model = Movie
        fields = "__all__"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    form = MovieAdminForm
    list_display = ("id", "title", "slug", "year", "category", "created_at")
    list_filter = ("year", "category")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {"fields": ("title", "slug", "description", "year", "category")}),
        ("Mídia", {"fields": ("cover_url", "cover_upload", "trailer_url", "video_path")}),
        ("Metadados", {"fields": ("created_at",), "classes": ("collapse",)}),
    )
    readonly_fields = ("created_at",)

    def save_model(self, request, obj, form, change):
        # Primeiro salva para garantir slug
        super().save_model(request, obj, form, change)
        f = form.cleaned_data.get("cover_upload")
        if f:
            # Define caminho remoto: covers/movies/<slug>.<ext>
            name, ext = os.path.splitext(f.name)
            remote = f"covers/movies/{obj.slug or obj.id}{ext.lower()}"
            # Salva temporário em memória
            tmp_path = os.path.join(request._streaming, f.name) if hasattr(request, "_streaming") else None
            # Como não temos storage temp garantido, gravar em /tmp local
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(f.read())
                tmp.flush()
                public_url = upload_to_bunny(tmp.name, remote)
            obj.cover_url = public_url
            obj.save(update_fields=["cover_url"]) 


@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_active", "position", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title",)
    list_editable = ("is_active", "position")
    ordering = ("position", "-created_at")