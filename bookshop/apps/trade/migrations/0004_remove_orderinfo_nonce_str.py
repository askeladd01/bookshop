# Generated by Django 3.2.5 on 2021-07-31 22:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0003_ordergoods_real_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderinfo',
            name='nonce_str',
        ),
    ]