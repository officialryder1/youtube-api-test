# Generated by Django 5.0.6 on 2024-05-12 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_post_category_post_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]
