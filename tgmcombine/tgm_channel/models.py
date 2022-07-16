from django.db import models

import operator
from itertools import chain

class CatName(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название категорий', blank=True, default=None)

    def __str__(self):
        return f'{self.name}'

    def meta_data(self):
        return {
            'title': f'Все телеграм каналы категории  {self.name} '
        }

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class CategoriesMatch(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название категорий', blank=True, default=None)
    name_id = models.ForeignKey(CatName, on_delete=models.SET_NULL, null=True)
    donor_categories_name = models.CharField(max_length=255, default='', verbose_name='Название категории у донора')
    keywords = models.CharField(max_length=255, default=None, verbose_name='Ключевые слова категории', blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Соответствие категорий'
        verbose_name_plural = 'Соответствие категорий'


class TgmChannel(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование канала')
    tgmlink = models.CharField(max_length=255, verbose_name='Cсылка на телеграмм', default='', unique=True,
                               error_messages={'unique':"Данный канал уже есть на нашем сайте."})
    description = models.CharField(max_length=255, verbose_name='Описание канала', default='')
    subs = models.IntegerField(verbose_name='Кол-во подписчиков', null=True, blank=True)
    logo = models.ImageField(verbose_name='Лого канала', upload_to="channel_logo/", blank=True)
    categories_match = models.ManyToManyField(CategoriesMatch, related_name='channel')
    active = models.BooleanField(verbose_name='Активен ли канал', blank=True, default=False)
    LastUpdate = models.DateField(verbose_name='Дата последнего обновления',  auto_now=False, default='1900-01-01')

    def tgm_real_link(self):
        return f'http://t.me/{self.tgmlink.split("@")[1]}'

    # Первая версия "похожих каналов". Логика:
    #1) берем каналы из той же категории
    #2)немного больше и немного меньше по подписчикам
    #3) оставляем нужное кол-во и выравливаем  по порядку от больше к меньшему
    def similar_channels(self):
        SIMILAR_CHANNELS_COUNT = 10
        simchahalf = int(SIMILAR_CHANNELS_COUNT/1.5)

        catid = CategoriesMatch.objects.get(pk=self.pk).name_id_id
        channels_id = CategoriesMatch.objects.filter(name_id_id=catid)
        similar_channels1 = \
            TgmChannel.objects.filter(pk__in=channels_id, subs__lt=self.subs).order_by('-subs')[:SIMILAR_CHANNELS_COUNT]
        similar_channels2 = \
            TgmChannel.objects.filter(pk__in=channels_id, subs__gt=self.subs).order_by('subs')[:SIMILAR_CHANNELS_COUNT]

        similar_channels = list(reversed(list(chain(reversed(list(similar_channels1[:simchahalf])),
                                               similar_channels2[:simchahalf]))))
        print(type(similar_channels))
        return similar_channels[:10]

    #
    #Перед сохранением нового канала проверяем его написание.
    #
    def check_new_channel(self):
        if self.tgmlink[0:12] == 'https://t.me':
            self.tgmlink = self.tgmlink[13:]
        if self.tgmlink[0:4] == 't.me':
            self.tgmlink = self.tgmlink[5:]
        if self.tgmlink[0] != '@':
            self.tgmlink = '@' + self.tgmlink
        return True

    #
    # Формируем мета теги страницы
    #
    def meta_data(self):
        return {
            'title': f'Телеграм канал {self.name} подписчиков {self.subs}'
        }

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Канал'
        verbose_name_plural = 'Каналы'


# присваиваем категории
def assign_cat():
    wo_cat = CategoriesMatch.objects.all()
    for obj in wo_cat:
        print(f'{obj.pk}) {obj.donor_categories_name}')
        search_cat = obj.donor_categories_name
        if search_cat == 'Рукоделие': search_cat= 'Хобби'
        try:
            cat = CatName.objects.get(name__contains=search_cat)
        except:
            cat = CatName.objects.get(name__contains='Другое')
        obj.name_id = cat
        obj.save()

    return wo_cat


#