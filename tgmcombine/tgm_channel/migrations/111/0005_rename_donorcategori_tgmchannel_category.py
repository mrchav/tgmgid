# Generated by Django 4.0.3 on 2022-04-06 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tgm_channel', '0004_remove_categories_tgmchannel_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tgmchannel',
            old_name='DonorCategori',
            new_name='Category',
        ),
    ]
