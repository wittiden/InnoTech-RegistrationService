## InnoTech RegistrationService (тестовое задание)

### Требования:
каждый выбирает по силам, это может быть python + django + djoser, python + fast api, keyckloak + python для самых продвинутых.

Приложение: регистрация (логин - email, password)) проверка email на валидность и отправляем на него ссылку, при переходе по ссылке - пользователь авторизуется в системе. БД- любая кроме sqllite, если кто-то обернет в Docker - отдельный респект.

___

## Мой стек технологий в связке Python+FastAPI+Keycloak

* fastapi~=0.141.1 - основной фрейм
* uvicorn~=0.53.0 - сервер для запуска
* dishka~=1.10.1 - удобный контейнер для хранения зависимостей и реализации DI
* python-keycloak~=7.1.1 - сервис по авторизации и управлению токенами


* pydantic[email]~=2.13.5 - валидация
* pydantic-settings~=2.15.0 - валидация со скрепом из env


* sqlalchemy~=2.0.54 - орм для работы с бд
* asyncpg~=0.31.0 - асинхронный движек бд


* loguru~=0.7.3 - логирование
___


## Поднимаемые в docker сервисы

* app - 8000 (само приложение)
* app_postgres - 5432 (postgresql база данных для самого приложения, настроен конфиг, контейнер, подключение, движок и сессии. В приложении не используется, но полностью готовка к работе)


* keycloak_postgres - 5433 (postgresql база данных в которую записывается keyclaok)
* keycloak - 8080, 9000 (сам keycloak сервис, который реализует модуль авторизации)

* pgadmin - 5050 (админка для визуализации наших бд)
___


## Дополнительно используются 

* logger, timeout middlewares - для нормального логирования поступающих запросов, дополнения заголовков необходимой информацией и контроля зависших ручек


* global exception handler - для создания единого стандарта по обработке и выводу ошибок


* lifespan - для контроля за жизненным циклом приложения
___

### Структура проекта

* bootstrap/ - хранит в себе все зависимости и настройки всех роутeров, middlewares, сборки и подключения этого всего к самому приложению


* common/ - для настроек, модулей/функций, которые используются во всем приложении

* container/ - для сборки dishka контейнера с зависимостями

* infrastructure/
  * database/ - хранит все необходимые конфиги и настройки бд
  * http/ - хранит в себе lifespan, middlewares, можно расширить healthcheck ручками
  * keycloak/ - хранит все необходимые конфиги и настройки keycloak + интеграцию со встроенным в сервис SMTP

    
* modules/
  * auth - модуль реализации операций по аутентификации
  * users - модуль реализации операций по работе с пользователем 

каждый модуль подразделяется на 

* api/ - реализация работы с ручками
* service/ - бизнес логика
* contracts/ - схемы и дто
* exceptions - кастомные исключения

___

## Для развертывания необходимо 


* создать свой env файл основываясь на:

      ENVIRONMENT=dev
      PROJECT_VERSION=1.0
      
      APP_SERVER_PORT=8000
      
      APP_DB_USER= #postgres
      APP_DB_PASS= #admin
      APP_DB_HOST=app_postgres
      APP_DB_PORT=5432
      APP_DB_NAME=registration_service_dev
      
      KC_DB_USER= #postgres
      KC_DB_PASS= #admin
      KC_DB_HOST=kс_postgres
      KC_DB_PORT=5433
      KC_DB_NAME=keycloak_dev
      
      KC_PORT=8080
      KC_ADMIN_USERNAME=admin
      KC_ADMIN_PASSWORD=admin
      
      KC_URL=http://keycloak:8080
      KC_REALM=registration-service-realm
      KC_CLIENT_ID=registration-service-client
      KC_ADMIN_ID=registration-service-admin
      KC_CLIENT_SECRET= #скопировать по пути описанном ниже
      KC_ADMIN_SECRET= #скопировать по пути описанном ниже
      
      PGADMIN_EMAIL= #admin@example.com
      PGADMIN_PASS= #admin
      PGADMIN_PORT=5050

* Везде где написано скопировать по пути пока пропустить 


* Запустить контейнеры - docker compose up
* Открыть - http://localhost:8080/
* В меню переходим на - registration-service-realm -> clients -> registration-service-admin -> credentials -> копируем секрет и вставляем в KC_ADMIN_SECRET
* Внутри - registration-service-admin -> Service accounts roles -> Assign role -> пишем в поиск - manage-users и добавляем эту роль 
* В меню переходим на - registration-service-realm -> clients -> registration-service-client -> credentials -> копируем секрет и вставляем в KC_CLIENT_SECRET


* при желании запустить контейнеры вместе с pgadmin 
 
  docker compose --profile pgamin up
