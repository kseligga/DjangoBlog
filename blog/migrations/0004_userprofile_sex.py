# Generated by Django 4.2.7 on 2024-01-18 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_userprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="sex",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]