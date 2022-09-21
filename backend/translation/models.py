import uuid

from django.contrib.auth import get_user_model
from django.db import models
from transcript.models import Transcript

from .metadata import LANGUAGE_CHOICES

UPDATED_MACHINE_GENERATED = "umg"
MACHINE_GENERATED = "mg"
MANUALLY_CREATED = "mc"

TRANSLATION_TYPE_CHOICES = (
    (MACHINE_GENERATED, "Machine Generated"),
    (UPDATED_MACHINE_GENERATED, "Updated Machine Generated"),
    (MANUALLY_CREATED, "Manually Created"),
)


class Translation(models.Model):
    """
    Translation model
    """

    translation_uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name="Translation UUID",
        primary_key=False,
    )
    translation_type = models.CharField(
        choices=TRANSLATION_TYPE_CHOICES, max_length=3, verbose_name="Translation Type"
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        default=None,
        on_delete=models.PROTECT,
        verbose_name="Parent Translation",
    )
    transcript = models.ForeignKey(
        Transcript,
        on_delete=models.CASCADE,
        verbose_name="Translation Transcript",
        related_name="translations",
    )
    target_language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=4, verbose_name="Target Language"
    )
    user = models.ForeignKey(
        get_user_model(),
        verbose_name="Translator",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    payload = models.JSONField(verbose_name="Translation Output")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Translation Created At"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Translation Updated At"
    )

    def __str__(self):
        return "Translation: " + str(self.translation_uuid)
