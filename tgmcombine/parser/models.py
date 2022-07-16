from django.db import models
import datetime
import urllib.request
import requests
from bs4 import BeautifulSoup
from tgm_channel.models import TgmChannel
from tgm_channel.models import CategoriesMatch
from django.db.models import Q


class donor_tlgrm_ru(models.Model):
    domain = models.CharField(max_length=100, verbose_name='Домен донора', default='https://tlgrm.ru')
    url = models.CharField(max_length=255, verbose_name='Основной URL', default='', null=True)
    LastUpdateData = models.DateTimeField(verbose_name='Дата последнего обновления', null=True, default=None)

    def __str__(self):
        return f'{self.domain}{self.url}'

    class Meta:
        verbose_name = 'Донор tlgrm_ru'
        verbose_name_plural = 'Донор tlgrm_ru'

    def get_urls(self, target_url):
        self.LastUpdateData= datetime.datetime.now()
        self.save()
        links_in_base = list(donor_tlgrm_ru.objects.all().filter(Q(LastUpdateData__lt=datetime.datetime.now() -
                                                                         datetime.timedelta(days=3)) |
                                                    Q(LastUpdateData=None)).values_list('url', flat=True))
        try:
            f = urllib.request.urlopen(target_url)
        except:
            f = False
        if f:
            soup = BeautifulSoup(f, 'html.parser')
            if len(target_url.split("@")) > 1:
                self.pars_channel_page(soup)
            links_in_page = []
            for link in soup.find_all('a'):
                li = link.get('href')
                if li is not None:
                    print(li[16:])
                    if li[16:] not in links_in_page and li[16:] not in links_in_base and li.find('channels') != -1\
                            and li.find('tlgrm.ru') == 8:
                        links_in_page.append(li[16:])

                    if li[16:] not in links_in_page and li.find('channels') == 17 and \
                            li.find('@') == -1 and li.find('?') == -1 and len(li) > 25:
                        print(f'----------перед циклом страниц')
                        for i in range(2,50):
                            str = f'{li[16:]}?page={i}'
                            print(f' перебираем {i}')
                            if str not in links_in_base:
                                links_in_page.append(str)
            # добавляем новые уникальные ссылки в базу
            for link in links_in_page:

                donor_tlgrm_ru.objects.create(url=link)



    #
    #парсим страницу с ТГМ каналом
    #
    def pars_channel_page(self, soup):
        #находим название канала
        name = soup.h1.text.lstrip().rstrip()
        print(f'название канала:{name}')
        #находим кол-во подписчиков
        subsc = soup.find("span", {"class": "channel-header__subscribers"}).text.lstrip().rstrip()
        print(f'колв-о подписчиков:{subsc}')
        #категория тгм канала
        cat_str = soup.find("a", {"class": "channel-header-nav js-back"}).text.lstrip().rstrip()
        donor_cat = cat_str[cat_str.find("«")+1:cat_str.find("»")]
        print(f'категория:{donor_cat}')
        #описание канала
        desc = soup.find("p", {"class": "channel-header__description"}).text.lstrip().rstrip()
        print(f'описание:{desc}')

        channel_logo = soup.find("img", {"class": "channel-header-avatar__image"})["src"]
        #ссылка на логотип
        print(f'картинка:{channel_logo}')

        #формируем название картики по формуле - ссылка канала без @ +текущая дата
        channel_url = soup.find("a", {"class": "channel-header__username"}).text.split("@")[1].lstrip().rstrip()
        logo_path = f'{channel_url}_{datetime.datetime.now().strftime("%Y_%m_%d")}.{channel_logo.split(".")[-1].split("?")[0]}'
        channel_url = f'@{channel_url}'
        #скачиваем по ссылке картинку и загружаем в каталог на сервере
        p = requests.get(channel_logo)
        out = open(f"media\channel_logo\{logo_path}", "wb")
        out.write(p.content)
        out.close()
        print(f'channel_logo/{logo_path}')
        #print(len(TgmChannel.objects.filter(tgmlink = channel_url)))

        if len(TgmChannel.objects.filter(tgmlink = channel_url)) == 0:
            print('добавление информации по новому каналу')
            cat = CategoriesMatch(name='', donor_categories_name=donor_cat, keywords='')
            cat.save()
            TgmChannel.objects.create(name=name, tgmlink=channel_url, description=desc, subs=subsc,
                                      logo=f'channel_logo/{logo_path}').categories_match.add(cat)








