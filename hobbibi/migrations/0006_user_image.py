# Generated by Django 3.0.8 on 2020-10-13 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hobbibi', '0005_auto_20200921_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
