# Generated by Django 4.0.2 on 2022-04-14 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("circle", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="desc",
            field=models.CharField(
                blank=True, max_length=64, null=True, verbose_name="描述信息"
            ),
        ),
    ]