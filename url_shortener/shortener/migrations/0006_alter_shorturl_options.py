# Generated by Django 5.1.6 on 2025-06-04 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0005_remove_shorturl_link'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shorturl',
            options={'ordering': ['-created_at']},
        ),
    ]
