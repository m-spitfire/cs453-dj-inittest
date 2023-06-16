# Generated by Django 4.2.1 on 2023-06-16 08:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="votes",
        ),
        migrations.RemoveField(
            model_name="post",
            name="votes",
        ),
        migrations.RemoveField(
            model_name="subreddit",
            name="subs",
        ),
        migrations.AddField(
            model_name="comment",
            name="votes",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.m2muser",
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="votes",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.m2muser",
            ),
        ),
        migrations.AddField(
            model_name="subreddit",
            name="subs",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.m2muser",
            ),
        ),
    ]
