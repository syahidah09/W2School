# Generated by Django 3.1.7 on 2021-11-08 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ewallet', '0011_auto_20211109_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ewallet.student'),
        ),
    ]