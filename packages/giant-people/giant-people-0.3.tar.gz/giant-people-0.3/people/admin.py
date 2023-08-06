from django.contrib import admin

from . import models


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    """
    Admin for Person model
    """

    list_display = ["name", "job_role", "order", "is_published"]
    search_fields = ["name", "job_role"]
    list_editable =  ["order"]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    fieldsets = [
        (None, {"fields": ["name", "job_role", "order", "image", "summary"]}),
        ("Contact", {"fields": ["email", "phone_number", "linkedin_url"]}),
        ("Publish", {"fields": ["is_published", "publish_at"]}),
        ("Meta Data", {"classes": ("collapse",), "fields": ["created_at", "updated_at"]},),
    ]
