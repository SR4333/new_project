# Generated by Django 3.2.11 on 2022-02-17 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temp_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='up_date',
            field=models.DateField(auto_now=True),
        ),
    ]