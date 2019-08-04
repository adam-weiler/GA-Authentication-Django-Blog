# Generated by Django 2.2.3 on 2019-08-04 18:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20190804_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='published_date',
            field=models.DateField(default=datetime.datetime(2019, 8, 4, 18, 53, 9, 79079)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 4, 18, 53, 9, 80061, tzinfo=utc)),
        ),
    ]