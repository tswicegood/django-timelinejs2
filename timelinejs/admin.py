from django.contrib import admin

from . import models


class TimelineEntryInline(admin.TabularInline):
    model = models.TimelineEntry


class TimelineAdmin(admin.ModelAdmin):
    inlines = [
        TimelineEntryInline,
    ]

    prepopulated_fields = {
        'slug': ('headline', ),
    }


admin.site.register(models.Asset)
admin.site.register(models.Timeline, TimelineAdmin)
