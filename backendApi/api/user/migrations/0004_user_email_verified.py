# Generated by Django 3.1.1 on 2020-10-08 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_reset_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_verified',
            field=models.CharField(default=0, max_length=5),
        ),
    ]
