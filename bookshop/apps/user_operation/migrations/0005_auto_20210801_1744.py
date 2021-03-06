# Generated by Django 3.2.5 on 2021-08-01 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0004_auto_20210801_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='address',
            field=models.CharField(max_length=100, verbose_name='详细地址'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='city',
            field=models.CharField(max_length=100, verbose_name='城市'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='district',
            field=models.CharField(max_length=100, verbose_name='区域'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='province',
            field=models.CharField(max_length=100, verbose_name='省份'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='signer_mobile',
            field=models.CharField(max_length=11, verbose_name='手机号码'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='signer_name',
            field=models.CharField(max_length=100, verbose_name='收件人'),
        ),
    ]
