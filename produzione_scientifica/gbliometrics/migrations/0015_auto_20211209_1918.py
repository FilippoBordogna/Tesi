# Generated by Django 3.2.9 on 2021-12-09 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gbliometrics', '0014_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='full_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='author',
            name='surname',
            field=models.CharField(max_length=50),
        ),
    ]
