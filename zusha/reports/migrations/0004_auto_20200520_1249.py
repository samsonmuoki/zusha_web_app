# Generated by Django 3.0.6 on 2020-05-20 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_auto_20200520_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='driver',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
