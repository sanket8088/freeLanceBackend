# Generated by Django 3.1.1 on 2020-09-17 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reset_key',
            field=models.CharField(default=0, max_length=500),
        ),
    ]
