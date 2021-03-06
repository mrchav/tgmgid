# Generated by Django 3.2.12 on 2022-04-13 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='donor_tlgrm_ru',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(default='https://tlgrm.ru', max_length=100, verbose_name='Домен донора')),
                ('url', models.CharField(default='', max_length=255, null=True, verbose_name='Основной URL')),
                ('LastUpdateData', models.DateTimeField(default=None, null=True, verbose_name='Дата последнего обновления')),
            ],
            options={
                'verbose_name': 'Донор tlgrm_ru',
                'verbose_name_plural': 'Донор tlgrm_ru',
            },
        ),
    ]
