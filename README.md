Инструкция по установке.
Заполнить файл .env своими данными как в примере .env.sample
Применить миграции
python manage.py migrate
Установить суперюзера и менеджера
python manage.py csu
python manage.py create_manager
Загрузить фикстуры
python manage.py loaddata data.json
Раcкомментировать строчки в distribution/views.py 22, 59-64 и services.py 64




