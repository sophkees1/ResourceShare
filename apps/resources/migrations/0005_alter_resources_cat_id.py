# Generated by Django 4.2.4 on 2023-08-24 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("resources", "0004_review"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resources",
            name="cat_id",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="resources.category",
            ),
        ),
    ]
