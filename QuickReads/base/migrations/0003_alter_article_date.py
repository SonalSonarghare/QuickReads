# Generated by Django 4.2.5 on 2024-04-26 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_bookmark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='Date',
            field=models.DateTimeField(),
        ),
    ]
