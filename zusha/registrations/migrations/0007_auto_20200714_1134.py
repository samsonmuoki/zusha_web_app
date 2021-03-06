# Generated by Django 3.0.6 on 2020-07-14 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0006_saccovehicle_date_registered'),
    ]

    operations = [
        migrations.AddField(
            model_name='registereddriver',
            name='license_categories',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G')], default='C', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='registereddriver',
            name='license_status',
            field=models.CharField(choices=[('Approved', 'Approved to operate'), ('Expired', 'License not renewed'), ('Blacklisted', 'Not approved to operate')], default='Approved', max_length=32),
        ),
        migrations.AlterField(
            model_name='sacco',
            name='license_status',
            field=models.CharField(choices=[('Approved', 'Approved to operate'), ('Expired', 'License not renewed'), ('Blacklisted', 'Not approved to operate')], default='Approved', max_length=32),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='inspection_status',
            field=models.CharField(choices=[('Approved', 'Approved to operate'), ('Expired', 'License not renewed'), ('Blacklisted', 'Not approved to operate')], default='Approved', max_length=32),
        ),
    ]
