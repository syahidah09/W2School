# Generated by Django 3.2 on 2021-12-25 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ewallet', '0003_alter_transaction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(),
        ),
    ]