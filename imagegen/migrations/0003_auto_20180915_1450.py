# Generated by Django 2.1.1 on 2018-09-15 14:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagegen', '0002_remove_generatedimage_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='generatedimage',
            options={'get_latest_by': '-viewed_at', 'ordering': ['-created_at'], 'verbose_name': 'Generated Image record', 'verbose_name_plural': 'Generated Image records'},
        ),
        migrations.AddField(
            model_name='generatedimage',
            name='created_at',
            field=models.DateTimeField(auto_created=True, blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='generatedimage',
            name='viewed_at',
            field=models.DateTimeField(blank=True, default=None),
        ),
        migrations.AlterIndexTogether(
            name='generatedimage',
            index_together={('created_at', 'viewed_at')},
        ),
    ]