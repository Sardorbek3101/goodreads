# Generated by Django 4.1.4 on 2023-02-08 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0004_alter_friendchat_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendshiprequest',
            name='view',
            field=models.BooleanField(default=False),
        ),
    ]