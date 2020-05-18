# Generated by Django 3.0.6 on 2020-05-18 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0002_auto_20200518_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saccodriver',
            name='driver',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='registrations.Driver'),
        ),
        migrations.AlterField(
            model_name='saccovehicle',
            name='vehicle',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='registrations.Vehicle'),
        ),
    ]
