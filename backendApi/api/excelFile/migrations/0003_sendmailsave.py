# Generated by Django 3.1.3 on 2020-12-01 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('excelFile', '0002_response_response'),
    ]

    operations = [
        migrations.CreateModel(
            name='SendMailSave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=500, null=True)),
                ('instructions', models.CharField(blank=True, max_length=500, null=True)),
                ('attention', models.CharField(blank=True, max_length=500, null=True)),
                ('message', models.CharField(blank=True, max_length=500, null=True)),
                ('footer', models.CharField(blank=True, max_length=500, null=True)),
                ('toMail', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'MailSend',
            },
        ),
    ]