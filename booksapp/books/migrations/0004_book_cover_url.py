# Generated by Django 4.0.1 on 2022-01-18 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_book_isbn'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover_url',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
