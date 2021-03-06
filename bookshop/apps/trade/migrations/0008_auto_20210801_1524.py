# Generated by Django 3.2.5 on 2021-08-01 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0007_alter_orderinfo_post_script'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='address',
            field=models.CharField(max_length=100, verbose_name='收货地址'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='signer_name',
            field=models.CharField(max_length=20, verbose_name='收件人'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='nums',
            field=models.IntegerField(default=1, verbose_name='购买数量'),
        ),
    ]
