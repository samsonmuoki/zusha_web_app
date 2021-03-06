# Generated by Django 3.0.6 on 2020-06-15 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_dailydriverreport_regno'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailydriverreport',
            name='ntsa_action',
            field=models.CharField(choices=[('Pending', 'No action was taken'), ('In-Progress', 'Currently being resolved'), ('Resolved', 'Corrective Action was taken')], default='Pending', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dailydriverreport',
            name='ntsa_action_description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
