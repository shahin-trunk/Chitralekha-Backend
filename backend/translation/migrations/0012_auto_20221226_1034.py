# Generated by Django 3.2.16 on 2022-12-26 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("transcript", "0011_alter_transcript_payload"),
        ("translation", "0011_alter_translation_parent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="translation",
            name="payload",
            field=models.JSONField(null=True, verbose_name="Translation Output"),
        ),
        migrations.AlterField(
            model_name="translation",
            name="transcript",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="translations",
                to="transcript.transcript",
                verbose_name="Translation Transcript",
            ),
        ),
    ]
