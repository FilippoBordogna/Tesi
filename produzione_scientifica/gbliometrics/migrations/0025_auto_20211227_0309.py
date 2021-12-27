# Generated by Django 3.2.9 on 2021-12-27 02:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gbliometrics', '0024_auto_20211213_0032'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliation',
            name='author_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='affiliation',
            name='document_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='agroup',
            name='authors',
            field=models.ManyToManyField(blank=True, to='gbliometrics.Author'),
        ),
        migrations.AlterField(
            model_name='snapshot',
            name='creation',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 27, 3, 9, 2, 881123)),
        ),
    ]
