# Курсовая работа №6
### Курс "Django"


## Сервис e-mail рассылок
Чтобы удержать текущих клиентов, часто используют вспомогательные, или «прогревающие», рассылки для информирования и привлечения клиентов.
Разработайте сервис управления рассылками, администрирования и получения статистики.

## Описание задач
- Реализуйте интерфейс заполнения рассылок, то есть CRUD-механизм для управления рассылками.
- Реализуйте скрипт рассылки, который работает как из командой строки, так и по расписанию.
- Добавьте настройки конфигурации для периодического запуска задачи.
- Расширьте модель пользователя для регистрации по почте, а также верификации.
- Добавьте интерфейс для входа, регистрации и подтверждения почтового ящика.
- Реализуйте ограничение доступа к рассылкам для разных пользователей.
- Реализуйте интерфейс менеджера.
- Создайте блог для продвижения сервиса.





## Требования для работы программы
- Сервер PostgreSQL (локальный или удаленный) с имеющейся на нем, установленной по умолчанию, базой данных postgres
- Отредактированный файле example.env, находящийся в корневой директории проекта, согласно параметрам доступа к
имеющемуся серверу PostgreSQL. Затем этот файл необходимо переименовать в .env
- Установленные зависимости, указанные в файле pyproject.toml
- Необходимо действия:
  - создать на сервере PostgreSQL пустую базу данных с именем, указанном в файле .env (DATABASE_NAME)
  - применить к этой БД миграции из проекта командой python manage.py migrate
  - создать superuser'а командой python manage.py create_custom_super_user
  - создать в БД группу пользователей managers и присвоить ей кастомные права командой python manage.py create_user_group managers set_user_active_status set_schedule_active_status
  - заполнить БД тестовыми данными из файлов blog_data.json и mailing_data.json командами python manage.py loaddata blog_data.json и python manage.py loaddata mailing_data.json 


## Логика работы программы

1. Любой пользователь может зарегистрироваться в сервисе рассылок. Создавать, редактировать и удалять адреса email клиентов, тексты писем и расписание их рассылок. При этом пользователь может работать только с сущностями, которые создал он. Кроме того, он может просматривать отчеты о тех рассылках, которые отправляли письма созданные только им.
2. Любой, даже неавторизованный пользователь, может просматривать статьи в блоге. После авторизации, любой пользователь может создавать статьи. Но для их публикации требуется одобрение пользователя входящего в группу managers. При этом, за пользователем остается право редактировать и удалять созданные им статьи.
3. Пользователи из группы managers наделены правами блокировки других пользователей, отключения активных рассылок. Они могут просматривать списки всех адресов, сообщений, расписаний рассылки и отчеты о них но не могут их изменять и удалять.
4. Сервис рассылок позволяет рассылать письма согласно расписанию их рассылок в автоматическом режиме: через определенное количество минут (параметр CRONJOBS_PERIOD в файле settings.py), проверяются все расписания рассылок и выбираются письма для отправки согласно параметрам расписания. Для запуска рассылок в автоматическом режиме используется команда python manage.py crontab add. Для ручного азпуска используется команда python manage.py send_scheduled_emails.   

