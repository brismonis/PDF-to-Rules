# Generated by Django 3.2.4 on 2021-08-10 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generate', '0017_files_stm'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='evidence',
            field=models.TextField(blank=True, null=True),
        ),
    ]