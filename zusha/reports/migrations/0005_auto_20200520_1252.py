# Generated by Django 3.0.6 on 2020-05-20 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_auto_20200520_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='ntsa_resolution',
            field=models.CharField(choices=[('Pending', 'No action was taken'), ('In Progress', 'Currently being resolved'), ('Resolved', 'Corrective Action was taken')], default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='report',
            name='sacco_resolution',
            field=models.CharField(choices=[('Pending', 'No action was taken'), ('In Progress', 'Currently being resolved'), ('Resolved', 'Corrective Action was taken')], default='Pending', max_length=20),
        ),
    ]