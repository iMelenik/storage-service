from django.contrib import admin

from upload.models.file import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'uploaded_at', 'size', 'is_processed')
    readonly_fields = ('uploaded_at',)
    list_display_links = ('name',)

    def name(self, obj):
        return obj.file.name
