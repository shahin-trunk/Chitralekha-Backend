# Generated by Django 3.2.16 on 2022-11-24 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("video", "0008_video_project_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="language",
            field=models.CharField(
                choices=[
                    ("en", "English"),
                    ("hi", "Hindi"),
                    ("as", "Assamese"),
                    ("bn", "Bengali"),
                    ("brx", "Bodo"),
                    ("gu", "Gujarati"),
                    ("kn", "Kannada"),
                    ("ks", "Kashmiri"),
                    ("gom", "Konkani"),
                    ("mai", "Maithili"),
                    ("ml", "Malayalam"),
                    ("mr", "Marathi"),
                    ("mni", "Manipuri"),
                    ("ne", "Nepali"),
                    ("or", "Oriya"),
                    ("pa", "Punjabi"),
                    ("sa", "Sanskrit"),
                    ("sd", "Sindhi"),
                    ("si", "Sinhala"),
                    ("ta", "Tamil"),
                    ("te", "Telugu"),
                    ("ur", "Urdu"),
                ],
                default=1,
                max_length=4,
                verbose_name="Target Language",
            ),
            preserve_default=False,
        ),
    ]
