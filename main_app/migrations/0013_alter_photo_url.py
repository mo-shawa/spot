# Generated by Django 3.2.9 on 2021-12-16 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='url',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
