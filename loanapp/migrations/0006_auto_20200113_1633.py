# Generated by Django 3.0.2 on 2020-01-14 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanapp', '0005_auto_20200113_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address2',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Address line 2'),
        ),
    ]