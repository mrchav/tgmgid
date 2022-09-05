from django.shortcuts import render
from rest_framework import generics
from django.db.models import Q
import time
import datetime
from django.core.paginator import Paginator
import tgm_channel.models
from .models import CatName
from .models import TgmChannel
from .models import CategoriesMatch
from .forms import ChannelForm
from .serializers import ChannelSerializer

'''
главнвая страница
'''


def main_page(request):
    #   Достаем все категории
    categories_name = CatName.objects.all()

    #
    #   формируем список с 6 каналами из каждой категории,
    #   а также считаем сколько в каждой категории каналов.
    #
    cats = list()
    for cat in categories_name:
        channels = TgmChannel.objects.filter(id__in=CategoriesMatch.objects.filter(name_id=cat.id)
                                             .values_list('id', flat=True))
        cats.append({
            'cat_data': cat,
            'data': channels[:6],
            'count': channels.count,

        })
    return render(request, './main_page.html', {'cats': cats,
                                                })


#
# Категории каналов и пагинация
#
def category_page(request, category_id):
    category = CatName.objects.get(pk=category_id)
    channel_id = CategoriesMatch.objects.filter(name_id=category_id)
    channels = TgmChannel.objects.filter(id__in=channel_id)
    paginator = Paginator(channels, 30)
    page_number = request.GET.get('page')
    page_channels = paginator.get_page(page_number)

    return render(request, './category_page.html', {
        'meta_data': category.meta_data,
        'category': category,
        'channels': page_channels,
    })


#
# Cтраница канала
#

def channel_page(request, channel_id):
    categories_name = CatName.objects.all()
    channel = TgmChannel.objects.get(pk=channel_id)
    category = CatName.objects.get(pk=CategoriesMatch.objects.get(pk=channel_id).name_id_id)

    return render(request, './channel_page.html', {'meta_data': channel.meta_data,
                                                   'category': category,
                                                   'channel': channel,
                                                   'all_categories': categories_name,
                                                   'similarchannels': channel.similar_channels,
                                                   })


#
# страница канала
#
def add_channel(request):
    add_message = ''
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            new_channel = form.save(commit=False)
            if new_channel.check_new_channel():
                new_channel.save()
                add_message = f'Спасибо, ваш канал {new_channel.tgmlink} добавлен, мы проверим ваш канал и в ' \
                              f'ближайшее время добавим на сайт'
    else:
        form = ChannelForm()
        add_message = 'Добавьте телеграм канал в формате @telegram_kanal'

    data = {'form': form,
            'add_message': add_message,
            }

    return render(request, './add_channel_page.html', data)


def update_data(request):
    tgm_channel.models.assign_cat()

    return render(request, './test_page.html', {
    })


def about(request):
    return render(request, './about_page.html', {
    })


class ChannelAPIView(generics.ListAPIView):
    queryset = TgmChannel.objects.all()[0:10]
    serializer_class = ChannelSerializer
