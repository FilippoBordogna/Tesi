# Generated by Django 3.2.9 on 2021-12-10 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gbliometrics', '0017_alter_author_orcid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affiliation',
            name='creation',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='affiliation',
            name='last_update',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
