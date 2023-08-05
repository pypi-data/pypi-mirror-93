from django.core.validators import URLValidator
from django.db import models

from filer.fields.image import FilerImageField

from mixins.models import PublishingMixin, PublishingQuerySetMixin, TimestampMixin


class Person(TimestampMixin, PublishingMixin):
    """
    Represents a person object
    """

    name = models.CharField(max_length=255)
    job_role = models.CharField(max_length=255, blank=True)
    image = FilerImageField(related_name="person_image", null=True, on_delete=models.SET_NULL)
    summary = models.TextField(blank=True)

    # Contact/social details
    linkedin_url = models.URLField(
        help_text="Enter the full URL of the LinkedIn page",
        blank=True,
        validators=[
            URLValidator(
                schemes=["https"],
                regex="www.linkedin.com",
                message="Please enter the full URL of the LinkedIn page",
            )
        ],
    )
    phone_number = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)

    objects = PublishingQuerySetMixin.as_manager()

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"
        ordering = ["name"]

    def __str__(self):
        """
        Return string representation
        """
        return self.name
