# Generated by Django 3.2.6 on 2021-08-28 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'Student'},
        ),
        migrations.AlterModelOptions(
            name='tutor',
            options={'verbose_name': 'Tutor'},
        ),
    ]
