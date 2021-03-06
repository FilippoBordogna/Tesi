# Generated by Django 3.2.9 on 2021-12-09 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gbliometrics', '0011_alter_affiliation_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affiliation',
            name='address',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='affiliation',
            name='city',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='affiliation',
            name='country',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='affiliation',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='affiliation',
            name='postal_code',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='affiliation',
            name='state',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='affiliation',
            name='url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='agroup',
            name='other_info',
            field=models.TextField(max_length=200, null=True),
        ),
    ]
