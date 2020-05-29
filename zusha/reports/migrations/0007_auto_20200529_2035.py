# Generated by Django 3.0.6 on 2020-05-29 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_report_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackVehicleReports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regno', models.CharField(max_length=10)),
                ('sacco', models.CharField(max_length=20)),
                ('date', models.DateField()),
                ('count', models.IntegerField(default=0)),
                ('ntsa_action', models.CharField(choices=[('Pending', 'No action was taken'), ('In Progress', 'Currently being resolved'), ('Resolved', 'Corrective Action was taken')], max_length=20)),
                ('sacco_action', models.CharField(choices=[('Pending', 'No action was taken'), ('In Progress', 'Currently being resolved'), ('Resolved', 'Corrective Action was taken')], max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='report',
            name='sacco',
            field=models.CharField(max_length=20, null=True),
        ),
    ]