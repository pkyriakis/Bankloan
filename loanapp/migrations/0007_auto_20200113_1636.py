# Generated by Django 3.0.2 on 2020-01-14 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanapp', '0006_auto_20200113_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='cf_api_password',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='cf_api_user_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
