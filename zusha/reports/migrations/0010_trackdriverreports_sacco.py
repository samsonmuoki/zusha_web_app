# Generated by Django 3.0.6 on 2020-06-03 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0009_auto_20200531_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackdriverreports',
            name='sacco',
            field=models.CharField(default='WASAFI', max_length=20),
            preserve_default=False,
        ),
    ]