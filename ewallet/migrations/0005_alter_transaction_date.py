# Generated by Django 3.2 on 2021-12-25 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ewallet', '0004_alter_transaction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
