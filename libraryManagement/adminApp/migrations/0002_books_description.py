# Generated by Django 5.1.7 on 2025-03-18 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
