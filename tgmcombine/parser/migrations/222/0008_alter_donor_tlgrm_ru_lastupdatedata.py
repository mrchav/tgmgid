# Generated by Django 4.0.3 on 2022-04-06 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0007_alter_donor_tlgrm_ru_lastupdatedata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor_tlgrm_ru',
            name='LastUpdateData',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Дата последнего обновления'),
        ),
    ]
