# Generated by Django 3.2.12 on 2022-04-24 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgm_channel', '0008_auto_20220424_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tgmchannel',
            name='subs',
            field=models.IntegerField(blank=True, null=True, verbose_name='Кол-во подписчиков'),
        ),
    ]