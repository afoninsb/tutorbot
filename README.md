
# TutorBot

Многопользовательская платформа Telegram-ботов для автоматизации работы учителя и репетитора при подготовке к ОГЭ и ЕГЭ

[Подробнее о боте - Landingpage](https://studybot.fun/)

## Содержание
- [Введение](#start)
- [Стек технологий](#tech)
- [Инсталляция](#install)
- [Начало работы](#use)
- [Галерея](#gallery)


<a name="start"></a> 
## Введение

Данный проект создан в помощь педагогам и репетиторам при подготовке их учащихся к ЕГЭ. С его помощью Telegram-бот получает функционал, обеспечивающий раздачу заданий, сбор ответов и построение статистики.

Разделы административной панели:
 - Боты: добавление и настройка ботов, созданных с помощью [@BotFather](https://t.me/BotFather)
 - Учащиеся: управление учащимися
 - Контент: добавление категорий и заданий и управление ими
 - Статистика: статистика по категориям, заданиям и ученикам за различные временные промежутки
 - Рейтинг: рейтинг учащихся

Добавленный и настроенный бот рассылает задания по настроенному учителем расписанию. Задание для рассылки выбирается случайно из активных категорий.

<a name="tech"></a> 
## Стек технологий

**Server:** Python 3.10, Django 4.1

<a name="install"></a> 
## Инсталляция

### 1. Развёртываем Django-проект

По ssh зайти в домашнюю папку вашего сайта. В домашней папке вашего сайта (папка должна быть пуста):
```bash
  git clone git@github.com:afoninsb/tutorbot.git ./
  python3 -3.10 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
```
### 2. Настраиваем переменные
Переименовать файл _tutor_bot/.env.dist_ в _tutor_bot/.env_

В файле _tutor_bot/.env_:
```bash
# Код Django
SECRET_KEY=django-injrtyuygecure-k%yu756#j@g+t636456454y4yeqfu&yfso4!ci%s_&3mg5p
# Telegram ID Суперадмина
BIG_BOSS_ID=337470404
# Токен регистрационного бота
REGBOT_TOKEN=5963756302:AAGU7Esfy45tgwyrtj7srttEnumUctgjI
# Токен регистрационного бота для разработки
TEMP_REGBOT_TOKEN=5962239353:seghfasbf764gtfwvywagyubgutGYGFCluggtlT
# параметры подключения к базе данных
BD_NAME=bd_name
BD_USER=user_login_bd
BD_PASSWORD=bd_password
BD_HOST=localhost
# DEBUG - в разработке или в продакшене?
DEBUG=False
# NGROK - адрес для подключения локального бота через NGROK
NGROK=bflist6yilgfegfligi.ngrok.io
# Параметры подключения к sentry.io
SENTRY_DSN=https://34asdjfh34tr3qgtfo8tyg2dtlqgf72t3lf82976.ingest.sentry.io/4765764653523696
```

Переименовать файл _tutor_bot/tutor_bot/settings.py.template_ в _tutor_bot/tutor_bot/settings.py_

В файле _tutor_bot/tutor_bot/settings.py_:
```bash
# URL вашего сайта
ALLOWED_HOSTS = ['your_cite.com']
BASE_URL = 'https://your_cite.com'

# Количество оставшихся задач, меньше которого срабатывает алерт
ALERT_MIN_TASKS = 10
# Количество дней до окончания тарифа, чтобы выдать алерт
ALERT_END_TARIF = 3
# Количество учащихся в бесплатном тарифе = Количество учащихся + Сам админ-учитель (3+1=4 - 3 учащихся)
STUDENT_FREE_TARIF = 4
```
### 3. Выполняем миграции, собираем статику, создаём суперпользователя для доступа в админку Django
```bash
  cd tutor_bot
  python3 manage.py migrate
  python3 manage.py collectstatic
  python3 manage.py createsuperuser
```
### 4. Настраиваем задание cron
Настроить файл  _tutor_bot/cron/cron.py_ на ежечасный запуск.

<a name="use"></a> 
## Начало работы

### Суперадмин
1. Создать регистрационного бота с помощью с помощью [@BotFather](https://t.me/BotFather). Этот бот будет использоваться для регистрации преподавателей в системе.
2. Войти в этот бот и написать ему что-либо
3. Прописать его токен в файле _tutor_bot/.env_
4. Перезапустить сервер
5. Информацию о контенте системы можно наблюдать в админке Django https://your_site.com/admin

### Учитель
1. Зайти в ваш адмнистративный бот в Telegram и написать боту какое-либо сообщение
2. Пройти регистрацию
3. Суперадмину в этот бот придёт оповещение. Необходимо одобрить или отказать. Если одобрить, то учитель становится администратором бота на сайте
4. Нажать на кнопку клавиатуры _"Войти в административную панель"_
5. Создать рабочего бота с помощью с помощью [@BotFather](https://t.me/BotFather)
6. В разделе _Боты_ добавить его на сайте
7. Настроить расписание работы бота, его пароль и параметры работы
8. Добавить контент - категории и задания
9. Пригласить учащихся в рабочий бот
10. Запустить категории и бота, чтобы он начал выдавать задания

### Ученик
1. Войти в бот, указанный учителем
2. Написать ему что-либо
3. Пройти регистрацию
4. Учитель в административной панели одобрит ученика
5. Получать задания и давать правильные ответы

<a name="gallery"></a> 
## Галерея: админ. панель
<img src="http://studybot.fun/wp-content/uploads/2023/02/42b7c9cc-5178-40fc-b44b-c69d58003719.jpeg" width="400px">
<img src="http://studybot.fun/wp-content/uploads/2023/02/6ba71a4c-5d65-4ab9-9cec-f09fddfd1b31.jpeg" width="400px">
<img src="http://studybot.fun/wp-content/uploads/2023/02/8e20f8b5-8b54-44e0-90e9-d6c66caf68be.png" width="400px">
<img src="http://studybot.fun/wp-content/uploads/2023/02/678c58a1-f6ad-4476-aa4e-6b6592a11195.png" width="400px">
<img src="http://studybot.fun/wp-content/uploads/2023/02/e586811d-40a1-4355-aa45-063403e83a60.png" width="400px">
<img src="http://studybot.fun/wp-content/uploads/2023/02/beba6d70-7c8b-4af0-b957-7e4b52a33adb.png" width="400px">
<img src="http://studybot.fun/wp-content/uploads/2023/02/904ba376-c422-46ba-a280-0d5c21e89aba.png" width="400px">
<img src="http://studybot.fun/wp-content/uploads/2023/02/73146825-0b57-47d0-b4d1-7c6636636ae9.png" width="400px">
<img src="http://studybot.fun/wp-content/uploads/2023/02/1204b05a-1f6e-46e0-b398-c7841d422195.png" width="400px">
<img src="http://studybot.fun/wp-content/uploads/2023/02/a3f48c88-98d5-4e48-915a-1212ce1df3df.png" width="400px">
<img src="http://studybot.fun/wp-content/uploads/2023/02/bc7f97da-17c8-44ae-807c-6abed30c9883.png" width="400px">
<img src="http://studybot.fun/wp-content/uploads/2023/02/d1b84d31-16a1-4809-9610-133b3ae7eddb.png" width="400px">
