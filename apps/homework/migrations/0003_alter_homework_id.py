# Generated by Django 4.1.7 on 2023-02-26 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0002_studenthomework_remove_homework_is_submitted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]