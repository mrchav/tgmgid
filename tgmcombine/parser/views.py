from django.shortcuts import render
from .models import donor_tlgrm_ru
from django.db.models import Q
import time
import datetime
import tgm_channel


# Create your views here.
def start_parser(request):

    pages = donor_tlgrm_ru.objects.all().filter(Q(LastUpdateData__lt=datetime.datetime.now() -
                                                                     datetime.timedelta(days=15)) |
                                                Q(LastUpdateData=None))
    count = 0

    for page in pages:
        count += 1
        print(f' парсим страницу номер {count}\n ')
        page.get_urls(f'{page.domain}/{page.url}')
        time.sleep(0)
    return render(request, './pars_page.html', {'object_list': 'page',
                                                'date': datetime.datetime.now(),
                                                })

def pars_data(request):

    return render(request, './pars_data.html', {
                                                'date': datetime.datetime.now(),
                                                })



