о проекте
реализован парсер сайта https://tlgrm.ru/
    2 модели: TgmChannel- модель тгм канала
              donor_tlgrm_ru - страницы сайта, которые должны обновляться раз в несколько дней
настроил celery , добавил таск с регулярным обновлением информации с сайта
подключил redis через docker



надо реализовать
запуск скрипта обновления по расписанию
получать последнюю информацию с пабликов (посты, описание)
разделить каналы по категориям - первый шаг - будут использоваться категории донеров, далее котегории планируется парсить из контента паблика