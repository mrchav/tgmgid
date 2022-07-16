from tgmcombine.celery import app
from .models import donor_tlgrm_ru
import datetime
import time
from django.db.models import Q
import tgm_channel.models

#from .service import send


@app.task()
def star_parser():
    pages = donor_tlgrm_ru.objects.all().filter(Q(LastUpdateData__lt=datetime.datetime.now() -
                                                                     datetime.timedelta(days=15)) |
                                                Q(LastUpdateData=None))
    count = 0
    for page in pages:
        count += 1
        print(f' парсим страницу номер \n\n\n\n{count}')
        page.get_urls(f'{page.domain}/{page.url}')
        time.sleep(1)


@app.task()
def update_category():
    tgm_channel.models.assign_cat()