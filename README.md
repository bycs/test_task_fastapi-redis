Инструкция по запуску
==
* Необходимые пакеты:
>docker

>docker-compose

* Запуск

В терминале из корневой папки проекта запустите команды:
>sudo docker-compose build

>sudo docker-compose up

* Сервис будет доступен по адресу:
>http://0.0.0.0:8080
* Документация будет доступна по адресу:
>http://0.0.0.0:8080/docs

Ресурсы:
=
* /visited_links
>   Передача в сервис массива ссылок в POST-запросе.
    Временем их посещения считается время получения запроса сервисом.
    Формат даты - YYMMDDHHDD.
* Пример запроса
>{
"links": [
"https://ya.ru",
"https://ya.ru?q=123",
"funbox.ru",
"https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
]
}
* Пример ответа
>{
"status": "OK"
}
***

* /visited_domains
>   Получение GET-запросом списка уникальных доменов,
    посещенных за переданный интервал времени.
    Формат даты - YYMMDDHHDD.
* Пример запроса
>GET /visited_domains?datetime_from=2109010000&datetime_to=2110010000
* Пример ответа
>{
"domains": [
"ya.ru",
"funbox.ru",
"stackoverflow.com"
],
"status": "OK"
}