[![DNS Client](https://github.com/MatveyIvanov/DNS-Client/actions/workflows/dnsclient.yml/badge.svg)](https://github.com/MatveyIvanov/DNS-Client/actions/workflows/dnsclient.yml)
![codecov](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/MatveyIvanov/da8502c03cbe9b44e95867a78434b6b3/raw/3371f7c2f021ece0b8dd876a17c0177938ecc95f/DNSClientCoverage.json)

# Описание

Программа позволяет получить IP адрес по доменному имени.\
[Последняя консольная версия программы](https://github.com/MatveyIvanov/DNS-Client/releases/tag/v1.0.2-console)\
[Последняя GUI версия программы](https://github.com/MatveyIvanov/DNS-Client/releases/tag/v1.0.2-gui)\
Ниже приведена инструкция для разработки.

# Разработка

## Установка

Для использования утилиты необходимо иметь установленный python версии 3.8 и выше (возможно, работает с более ранними версиями, но это не проверено).
Также необходимо установить сторонние модули из файла requirements.txt. Рекомендуется создавать локальное окружение.

## Запуск

Для получения IP адреса доменного имени запустите скрипт из терминала с переданным доменным именем в качестве первого параметра

```
python dns.py www.example.com
```
