# Generated by Django 4.1.4 on 2022-12-29 12:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('storage', '0006_alter_profile_options_remove_profile_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
