# Generated by Django 3.2.4 on 2021-08-05 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generate', '0016_alter_files_pdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='stm',
            field=models.TextField(blank=True, null=True),
        ),
    ]
