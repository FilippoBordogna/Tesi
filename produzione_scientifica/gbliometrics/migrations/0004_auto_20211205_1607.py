# Generated by Django 3.2.9 on 2021-12-05 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbliometrics', '0003_rename_prova_authors_group'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Authors_Group',
            new_name='AuthorsGroup',
        ),
        migrations.AlterUniqueTogether(
            name='authorsgroup',
            unique_together={('user', 'name')},
        ),
    ]
