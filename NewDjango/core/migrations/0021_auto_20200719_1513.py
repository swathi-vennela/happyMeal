# Generated by Django 2.2.10 on 2020-07-19 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20200719_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='chef_key',
            field=models.CharField(default='19-Jul-2020 (15:13:37.986127)', max_length=100),
        ),
    ]