# Generated by Django 2.2.1 on 2019-06-21 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('JpipeApp', '0002_jp_device_data_voltage'),
    ]

    operations = [
        migrations.AddField(
            model_name='jp_devices',
            name='CUId',
            field=models.ForeignKey(db_column='CUId', default=1, on_delete=django.db.models.deletion.CASCADE, to='JpipeApp.JP_Company_Users'),
        ),
    ]