from django.contrib import admin

from upload.models import MediaFile


class MediaFileAdmin(admin.ModelAdmin):
    readonly_fields = ('unique_id', 'created_at')


admin.site.register(MediaFile, MediaFileAdmin)
