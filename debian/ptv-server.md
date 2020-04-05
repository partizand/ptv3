% PTV-SERVER(1)
% PARTIZAND
% April 2020

# NAME

Ptv-server. russian tv

# SYNOPSIS

**none**

# DESCRIPTION

Сервер собирающий потоки с разных сайтов. независимый от Коди. http://xbmc.ru/forum/showthread.php?t=16628

Особенности пакета

* Сервис стартует в изолированной среде, без прав root
* Настройки не перетираются при установке
* При каждом старте сервиса, настройки каналов архивируются в файл с номером дня недели

Располагается в /var/lib/ptv-server

Настройки /var/lib/ptv-server/user /var/lib/ptv-server/settings

При каждом старте сервиса, настройки каналов архивируются в /var/lib/ptv-server/backup файл с номером дня недели. Файлы перетираются.

/var/lib/ptv-server/backup можно архивировать/переносить в другое место во время работы сервиса.


Web-интерфейс сервера http://127.0.0.1:8185


# GENERAL OPTIONS

