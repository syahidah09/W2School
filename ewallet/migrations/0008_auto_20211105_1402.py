# Generated by Django 3.1.7 on 2021-11-05 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ewallet', '0007_auto_20211103_1951'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['student_id']},
        ),
    ]
