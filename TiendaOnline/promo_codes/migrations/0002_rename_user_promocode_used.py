# Generated by Django 4.2.7 on 2024-06-28 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("promo_codes", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="promocode",
            old_name="user",
            new_name="used",
        ),
    ]
