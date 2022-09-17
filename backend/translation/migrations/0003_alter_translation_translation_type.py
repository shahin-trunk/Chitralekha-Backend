# Generated by Django 4.0.5 on 2022-09-17 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translation', '0002_alter_translation_target_lang'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translation',
            name='translation_type',
            field=models.CharField(choices=[('he', 'Human Edited'), ('mg', 'Machine Generated'), ('mc', 'Manually Created')], max_length=2, verbose_name='Translation Type'),
        ),
    ]
