# Generated by Django 3.2.4 on 2021-06-30 15:29

from django.db import migrations, models
import generate.validators


class Migration(migrations.Migration):

    dependencies = [
        ('generate', '0014_alter_files_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='pdf',
            field=models.FileField(upload_to='pdfs/', validators=[generate.validators.validate_file_extension]),
        ),
    ]