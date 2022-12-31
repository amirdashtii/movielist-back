# Generated by Django 4.1.4 on 2022-12-31 22:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0008_alter_movie_imdbid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='list',
            name='user',
        ),
        migrations.AddField(
            model_name='list',
            name='profile',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.PROTECT, to='storage.profile'),
            preserve_default=False,
        ),
    ]
