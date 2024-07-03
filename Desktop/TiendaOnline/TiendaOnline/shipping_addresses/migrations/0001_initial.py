# Generated by Django 4.2.7 on 2024-06-03 14:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ShippingAddress",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("line1", models.CharField(max_length=200)),
                ("line2", models.CharField(blank=True, max_length=200)),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("country", models.CharField(max_length=50)),
                ("reference", models.CharField(blank=True, max_length=300)),
                ("postal_code", models.CharField(max_length=10)),
                ("default", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]