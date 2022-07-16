# Generated by Django 3.2.12 on 2022-04-13 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tgm_channel', '0007_alter_categories_keywords_alter_categories_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriesMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donor_categories_name', models.CharField(default='', max_length=255, verbose_name='Название категории у донора')),
                ('keywords', models.CharField(blank=True, default=None, max_length=255, verbose_name='Ключевые слова категории')),
            ],
            options={
                'verbose_name': 'Соответствие категорий',
                'verbose_name_plural': 'Соответствие категорий',
            },
        ),
        migrations.CreateModel(
            name='CatName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=30, verbose_name='Название категорий')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.RemoveField(
            model_name='tgmchannel',
            name='Category',
        ),
        migrations.AlterField(
            model_name='tgmchannel',
            name='tgmlink',
            field=models.CharField(default='', max_length=255, verbose_name='Cсылка на телеграмм'),
        ),
        migrations.DeleteModel(
            name='Categories',
        ),
        migrations.AddField(
            model_name='categoriesmatch',
            name='name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tgm_channel.catname'),
        ),
        migrations.AddField(
            model_name='tgmchannel',
            name='categories_match',
            field=models.ManyToManyField(to='tgm_channel.CategoriesMatch'),
        ),
    ]