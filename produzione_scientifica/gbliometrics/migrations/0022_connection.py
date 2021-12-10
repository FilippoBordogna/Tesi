# Generated by Django 3.2.9 on 2021-12-10 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gbliometrics', '0021_remove_author_orcid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gbliometrics.author')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gbliometrics.agroup')),
            ],
        ),
    ]