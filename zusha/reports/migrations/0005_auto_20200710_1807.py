# Generated by Django 3.0.6 on 2020-07-10 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_auto_20200615_0812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailydriverreport',
            name='ntsa_action',
            field=models.CharField(choices=[('Pending', 'No action was taken'), ('In Progress', 'Currently being resolved'), ('Resolved', 'Corrective Action was taken')], max_length=20),
        ),
        migrations.AlterField(
            model_name='dailyvehiclereport',
            name='ntsa_action',
            field=models.CharField(choices=[('Pending', 'No action was taken'), ('In Progress', 'Currently being resolved'), ('Resolved', 'Corrective Action was taken')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='dailyvehiclereport',
            name='sacco_action',
            field=models.CharField(choices=[('Pending', 'No action was taken'), ('In Progress', 'Currently being resolved'), ('Resolved', 'Corrective Action was taken')], default='Pending', max_length=20),
        ),
    ]
