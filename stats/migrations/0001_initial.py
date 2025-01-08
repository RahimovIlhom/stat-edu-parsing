# Generated by Django 5.1.4 on 2025-01-08 10:02

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otm_code', models.CharField(max_length=20, unique=True)),
                ('otm_name', models.CharField(max_length=255)),
                ('ownership_type', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='StatisticsSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('snapshot_date', models.DateField(default=django.utils.timezone.now)),
                ('bachelor_full_time', models.IntegerField(default=0)),
                ('bachelor_evening', models.IntegerField(default=0)),
                ('bachelor_part_time', models.IntegerField(default=0)),
                ('bachelor_special', models.IntegerField(default=0)),
                ('bachelor_joint', models.IntegerField(default=0)),
                ('bachelor_distance', models.IntegerField(default=0)),
                ('secondary_full_time', models.IntegerField(default=0)),
                ('secondary_evening', models.IntegerField(default=0)),
                ('secondary_part_time', models.IntegerField(default=0)),
                ('masters_full_time', models.IntegerField(default=0)),
                ('masters_evening', models.IntegerField(default=0)),
                ('masters_part_time', models.IntegerField(default=0)),
                ('masters_special', models.IntegerField(default=0)),
                ('masters_joint', models.IntegerField(default=0)),
                ('masters_distance', models.IntegerField(default=0)),
                ('total_students', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.institution')),
            ],
            options={
                'indexes': [models.Index(fields=['snapshot_date'], name='stats_stati_snapsho_4ca951_idx'), models.Index(fields=['institution', 'snapshot_date'], name='stats_stati_institu_3b66b8_idx')],
                'unique_together': {('institution', 'snapshot_date')},
            },
        ),
    ]
