# Generated by Django 3.0.3 on 2020-02-17 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_auto_20200215_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='license_status',
            field=models.CharField(choices=[('approved', 'Approved to operate'), ('blacklisted', 'Not approved to operate')], default='approved', max_length=32),
        ),
        migrations.AddField(
            model_name='sacco',
            name='license_status',
            field=models.CharField(choices=[('approved', 'Approved to operate'), ('blacklisted', 'Not approved to operate')], default='approved', max_length=32),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='license_status',
            field=models.CharField(choices=[('approved', 'Approved to operate'), ('blacklisted', 'Not approved to operate')], default='approved', max_length=32),
        ),
    ]