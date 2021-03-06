# Generated by Django 3.0.6 on 2020-06-21 09:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0003_auto_20200615_0714'),
    ]

    operations = [
        migrations.AddField(
            model_name='saccodriver',
            name='date_registered',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='saccodriver',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='saccodriver',
            name='last_status_update_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='saccodriver',
            name='status',
            field=models.CharField(choices=[('Approved', 'Approved to operate'), ('Suspended', 'Suspended for the time being'), ('Blacklisted', 'Blacklisted from operating')], default='Approved', max_length=20),
        ),
    ]
