# Generated by Django 4.1.4 on 2023-01-07 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_author_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='photo',
            field=models.ImageField(default='default_profile_pic.jpg', upload_to=''),
        ),
    ]