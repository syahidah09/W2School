# Generated by Django 3.1.7 on 2021-10-28 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ewallet', '0002_auto_20211026_0149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='transaction_id',
        ),
    ]