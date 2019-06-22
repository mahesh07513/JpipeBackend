# Generated by Django 2.2.1 on 2019-06-22 16:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('JpipeApp', '0004_jp_device_config_mapping'),
    ]

    operations = [
        migrations.CreateModel(
            name='JP_Adapter',
            fields=[
                ('AdapterId', models.AutoField(primary_key=True, serialize=False)),
                ('AdapterName', models.CharField(max_length=50, null=True)),
                ('DeviceMac', models.CharField(max_length=50, unique=True)),
                ('StatusActive', models.BooleanField(default=True)),
                ('Create_Date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('Change_Date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'JP_Adapter',
            },
        ),
    ]
