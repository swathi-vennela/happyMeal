# Generated by Django 2.2.10 on 2020-07-16 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_item_averagerating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='category',
        ),
        migrations.RemoveField(
            model_name='item',
            name='label',
        ),
        migrations.AddField(
            model_name='item',
            name='calories',
            field=models.FloatField(default=0),
        ),
    ]
